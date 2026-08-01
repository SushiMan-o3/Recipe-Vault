from fastapi import APIRouter, HTTPException, status
from schemas.auth import Token, UserCreate, UserLogin
from database import create_connection, close_connection

# do loadenv for bcyprts hashing algo, secret key, etc

route = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

def create_token():
    pass

def verify_password(plain_password, hashed_password):
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
        
        token = create_token()
        
        return {
            "access_token": token,
            "token_type": "bearer",
        }
        
    except:
        raise Exception("User authentication failed")


@route.post("/register", response_class=Token)
def register(user: UserCreate):
    pass
