from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from recipe_vault.config import FRONTEND_URL
from recipe_vault.database import init_db
from recipe_vault.routes import auth

app = FastAPI()

init_db()

origins = [FRONTEND_URL] if FRONTEND_URL else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.route)

@app.get("/")
def read_root():
    return ("Nothing here to talk about")

