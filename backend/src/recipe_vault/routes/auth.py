from fastapi import APIRouter
from schemas.auth import Token, UserCreate, UserLogin

# do loadenv for bcyprts hashing algo, secret key, etc

route = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@route.post("/login", response_model=Token)
def login(user: UserLogin):
    pass


@route.post("/register", response_class=Token)
def register(user: UserCreate):
    pass
