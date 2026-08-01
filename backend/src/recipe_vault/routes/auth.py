from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import APIRouter, HTTPException, status

from recipe_vault.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from recipe_vault.database import close_connection, create_connection
from recipe_vault.schemas.auth import Token, UserCreate, UserLogin


route = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


def create_jwt_auth_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.now(timezone.utc) + expires_delta
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(username: str) -> str:
    return create_jwt_auth_token(
        {"sub": username},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def get_user_from_token(token: str):
    pass


@route.post("/login", response_model=Token)
def login(user: UserLogin):
    if not user.user or not user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    conn = None
    cursor = None
    
    try:
        conn, cursor = create_connection()
        
        cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (user.user, user.user))
        user_data = cursor.fetchone()
        
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )        
            
        if not verify_password(user.password, user_data["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )
        
        token = create_access_token(user_data["username"])
        
        return {
            "access_token": token,
            "token_type": "bearer",
        }
        
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User authentication failed",
        )
    finally:
        close_connection(conn, cursor)


@route.post("/register", response_class=Token)
def register(user: UserCreate):
    
    conn, cursor = None, None
    
    try:
        conn, cursor = create_connection()
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User registration failed",
        )
    finally:
        close_connection(conn, cursor)


@route.put("/change-password")
def change_password(user: UserLogin):
    pass
