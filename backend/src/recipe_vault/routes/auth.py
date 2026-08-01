from fastapi import APIRouter, HTTPException, status
from schemas.auth import Token, UserCreate, UserLogin
import bcrypt
from database import create_connection, close_connection

# do loadenv for bcyprts hashing algo, secret key, etc

route = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

def create_token(user: str):
    pass


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
        
        token = create_token(user_data["username"])
        
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
        pass
    except:
        pass
    finally:
        close_connection(conn, cursor)

        
