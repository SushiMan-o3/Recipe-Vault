from fastapi import APIRouter, HTTPException, status
from schemas.auth import Token, UserCreate, UserLogin
import bcrypt
from database import create_connection, close_connection
from dotenv import load_dotenv
import os
import jwt
from datetime import datetime, timedelta, timezone


route = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


def create_jwt_auth_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.now(timezone.utc) + expires_delta
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(username: str) -> str:
    return create_jwt_auth_token(
        {"sub": username},
        timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES),
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
        
        close_connection(conn, cursor)
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
        
    except:
        raise Exception("User authentication failed")
    finally:
        close_connection(conn, cursor)


@route.post("/register", response_class=Token)
def register(user: UserCreate):
    
    conn, cursor = None, None
    
    try:
        conn, cursor = create_connection()
    except:
        raise Exception("User registration failed")
    finally:
        close_connection(conn, cursor)


@route.put("/change-password")
def change_password(user: UserLogin):
    pass
