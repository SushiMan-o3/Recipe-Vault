import re

from fastapi import APIRouter, HTTPException, status

from database import close_connection, create_connection
from schemas.auth import Token, UserCreate, UserLogin, forgotPasswordRequest
from services.security import create_access_token, hash_password, verify_password


route = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


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


@route.post("/register", response_model=Token)
def register(user: UserCreate):
    
    conn, cursor = None, None
    
    try:
        conn, cursor = create_connection()

        cursor.execute("SELECT * FROM users WHERE username = %s", (user.username,))
        existing_user = cursor.fetchone()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )

        cursor.execute("SELECT * FROM users WHERE email = %s", (user.email,))
        existing_user = cursor.fetchone()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already taken",
            )

        if not re.match(r"^[a-zA-Z0-9_.-]{3,20}$", user.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username must be 3-20 characters long and can only contain letters, numbers, underscores, hyphens, and periods",
            )

        if len(user.password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters long",
            )

        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&^#()_+\-=\[\]{};':\"\\|,.<>/?]).{8,}$", user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must contain at least one uppercase letter, one lowercase letter, and one number",
            )

        hashed_password = hash_password(user.password)

        cursor.execute(
            "INSERT INTO users (email, username, password) VALUES (%s, %s, %s) RETURNING *",
            (user.email, user.username, hashed_password),
        )
        new_user = cursor.fetchone()

        cursor.execute(
            "INSERT INTO additionaluserinfo (user_id) VALUES (%s)",
            (new_user["id"],),
        )

        conn.commit()

        token = create_access_token(new_user["username"])

        return {
            "access_token": token,
            "token_type": "bearer",
        }
    
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User registration failed",
        )
    finally:
        close_connection(conn, cursor)


@route.put("/forgot-password", response_model=None)
def forgot_password(email: forgotPasswordRequest):
    conn, cursor = None, None
    
    try:
        conn, cursor = create_connection()

        cursor.execute("SELECT * FROM users WHERE email = %s", (email.email,))
        existing_user = cursor.fetchone()

        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email not found",
            )

        # do some other stuff here, figure it out later 

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Forgot password failed",
        )
    finally:
        close_connection(conn, cursor)

