"""Shared test fixtures.

The whole suite runs without Postgres: the database layer is replaced with an
in-memory fake, so tests are fast and don't depend on a live server or leave
rows behind.
"""

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# The app uses flat imports ("from config import ...", "from schemas.auth import
# ..."), so src/recipe_vault itself has to be on sys.path, not just src.
SRC = Path(__file__).resolve().parents[1] / "src" / "recipe_vault"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import database  # noqa: E402

# main.py calls init_db() at import time, which would open a real connection.
# Stash the real one for test_main.py, then stub it out before importing main.
real_init_db = database.init_db
database.init_db = lambda: None

import main  # noqa: E402
import routes.auth as auth_routes  # noqa: E402


class FakeDB:
    """Stands in for the users table."""

    def __init__(self):
        self.users = []
        self.user_info = []
        self.pending = []
        self.pending_info = []
        self.next_id = 1

    def add(self, email, username, password):
        row = {
            "id": self.next_id,
            "email": email,
            "username": username,
            "password": password,
        }
        self.next_id += 1
        self.users.append(row)
        return row


class FakeCursor:
    def __init__(self, db):
        self._db = db
        self._result = []
        self.closed = False

    def execute(self, query, params=()):
        q = " ".join(query.lower().split())
        self._result = []

        if q.startswith("create table"):
            return

        if q.startswith("select"):
            if "username = %s or email = %s" in q:
                ident = params[0]
                self._result = [
                    r for r in self._db.users
                    if r["username"] == ident or r["email"] == ident
                ]
            elif "username = %s" in q:
                self._result = [r for r in self._db.users if r["username"] == params[0]]
            elif "email = %s" in q:
                self._result = [r for r in self._db.users if r["email"] == params[0]]
            return

        if q.startswith("insert into additionaluserinfo"):
            self._db.pending_info.append({"user_id": params[0]})
            return

        if q.startswith("insert into users"):
            email, username, password = params
            row = {
                "id": self._db.next_id,
                "email": email,
                "username": username,
                "password": password,
            }
            self._db.next_id += 1
            # Not visible to other connections until commit, same as Postgres.
            self._db.pending.append(row)
            self._result = [row]
            return

        raise AssertionError(f"FakeCursor received an unhandled query: {query}")

    def fetchone(self):
        return self._result[0] if self._result else None

    def fetchall(self):
        return list(self._result)

    def close(self):
        self.closed = True


class FakeConnection:
    def __init__(self, db):
        self._db = db
        self.closed = False
        self.commits = 0

    def cursor(self, *args, **kwargs):
        return FakeCursor(self._db)

    def commit(self):
        self.commits += 1
        self._db.users.extend(self._db.pending)
        self._db.user_info.extend(self._db.pending_info)
        self._db.pending.clear()
        self._db.pending_info.clear()

    def rollback(self):
        self._db.pending.clear()
        self._db.pending_info.clear()

    def close(self):
        self.closed = True


@pytest.fixture
def db():
    return FakeDB()


@pytest.fixture
def client(db, monkeypatch):
    """TestClient with the auth routes wired to the fake database."""

    def fake_create_connection():
        conn = FakeConnection(db)
        return conn, conn.cursor()

    monkeypatch.setattr(auth_routes, "create_connection", fake_create_connection)

    with TestClient(main.app) as test_client:
        yield test_client


@pytest.fixture
def seed_user(db):
    """Insert a user with a real bcrypt hash and return its plaintext credentials."""

    def _seed(
        username="testuser",
        email="test@example.com",
        password="Password1!",
    ):
        db.add(email, username, auth_routes.hash_password(password))
        return {"username": username, "email": email, "password": password}

    return _seed
