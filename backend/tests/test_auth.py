import pytest

VALID_PASSWORD = "Password1!"


def register_payload(**overrides):
    payload = {
        "email": "new@example.com",
        "username": "newuser",
        "password": VALID_PASSWORD,
    }
    payload.update(overrides)
    return payload


# --- login -----------------------------------------------------------------


def test_valid_login_email(client, seed_user):
    user = seed_user()

    response = client.post(
        "/auth/login",
        json={"user": user["email"], "password": user["password"]},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_valid_login_username(client, seed_user):
    user = seed_user()

    response = client.post(
        "/auth/login",
        json={"user": user["username"], "password": user["password"]},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_login_invalid_username(client, seed_user):
    seed_user()

    response = client.post(
        "/auth/login",
        json={"user": "nosuchuser", "password": VALID_PASSWORD},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"


def test_login_invalid_email(client, seed_user):
    seed_user()

    response = client.post(
        "/auth/login",
        json={"user": "nobody@example.com", "password": VALID_PASSWORD},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"


def test_login_invalid_password(client, seed_user):
    user = seed_user()

    response = client.post(
        "/auth/login",
        json={"user": user["username"], "password": "WrongPassword1!"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"


# --- register --------------------------------------------------------------


def test_register_valid(client, db):
    response = client.post("/auth/register", json=register_payload())

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]

    # The row is committed, and the password is hashed rather than stored raw.
    assert len(db.users) == 1
    stored = db.users[0]
    assert stored["username"] == "newuser"
    assert stored["email"] == "new@example.com"
    assert stored["password"] != VALID_PASSWORD


def test_register_existing_username(client, seed_user):
    seed_user(username="taken", email="taken@example.com")

    response = client.post(
        "/auth/register",
        json=register_payload(username="taken"),
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Username already taken"


def test_register_existing_email(client, seed_user):
    seed_user(username="someone", email="taken@example.com")

    response = client.post(
        "/auth/register",
        json=register_payload(email="taken@example.com"),
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already taken"


def test_register_invalid_username(client, db):
    # 21 chars, but the column is VARCHAR(20) - should be rejected before insert.
    response = client.post(
        "/auth/register",
        json=register_payload(username="a" * 21),
    )

    assert response.status_code in (400, 422)
    assert db.users == []

def test_register_invalid_username2(client, db):
    # Right length, but spaces and "!" are outside the allowed character set.
    response = client.post(
        "/auth/register",
        json=register_payload(username="bad user!"),
    )

    assert response.status_code == 400
    assert "Username must be 3-20 characters" in response.json()["detail"]
    assert db.users == []

def test_register_invalid_email(client, db):
    response = client.post(
        "/auth/register",
        json=register_payload(email="not-an-email"),
    )

    assert response.status_code == 422
    assert db.users == []


def test_register_invalid_password_not_long_enough(client, db):
    response = client.post("/auth/register", json=register_payload(password="Ab1!"))

    assert response.status_code == 400
    assert response.json()["detail"] == "Password must be at least 8 characters long"
    assert db.users == []


def test_register_invalid_password_no_uppercase(client, db):
    response = client.post(
        "/auth/register",
        json=register_payload(password="password1!"),
    )

    assert response.status_code == 400
    assert db.users == []


def test_register_invalid_password_no_lowercase(client, db):
    response = client.post(
        "/auth/register",
        json=register_payload(password="PASSWORD1!"),
    )

    assert response.status_code == 400
    assert db.users == []


def test_register_invalid_password_no_number(client, db):
    response = client.post(
        "/auth/register",
        json=register_payload(password="Password!"),
    )

    assert response.status_code == 400
    assert db.users == []


def test_register_invalid_password_no_special_char(client, db):
    response = client.post(
        "/auth/register",
        json=register_payload(password="Password1"),
    )

    assert response.status_code == 400
    assert db.users == []


# cant test forgot password because it requires sending an email and receiving a token, which is not feasible in a unit test environment
