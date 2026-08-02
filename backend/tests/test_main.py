import database
import pytest
from conftest import FakeConnection, FakeCursor, real_init_db


def test_read_root(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == "Nothing here to talk about"


def test_initialize_db(db, monkeypatch):
    conn = FakeConnection(db)
    cursor = conn.cursor()
    executed = []

    original_execute = cursor.execute
    monkeypatch.setattr(
        cursor,
        "execute",
        lambda query, params=(): (executed.append(query), original_execute(query, params))[1],
    )
    monkeypatch.setattr(database, "create_connection", lambda: (conn, cursor))

    real_init_db()

    assert len(executed) == 1
    assert "create table if not exists users" in " ".join(executed[0].lower().split())
    assert conn.commits == 1
    assert conn.closed and cursor.closed


def test_create_connection(db, monkeypatch):
    fake_conn = FakeConnection(db)
    monkeypatch.setattr(database.psycopg2, "connect", lambda dsn: fake_conn)

    conn, cursor = database.create_connection()

    assert conn is fake_conn
    assert isinstance(cursor, FakeCursor)


def test_create_connection_failure(db, monkeypatch):
    def boom(dsn):
        raise RuntimeError("no server")

    monkeypatch.setattr(database.psycopg2, "connect", boom)

    with pytest.raises(Exception, match="Database connection failed"):
        database.create_connection()


def test_close_connection(db):
    conn = FakeConnection(db)
    cursor = conn.cursor()

    database.close_connection(conn, cursor)

    assert cursor.closed
    assert conn.closed


def test_close_connection_accepts_none():
    # create_connection can hand back Nones, so close has to tolerate them.
    database.close_connection(None, None)
