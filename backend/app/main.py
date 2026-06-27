from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import init_db, get_db
from routes.auth import router as auth_router
from routes.recipes import router as recipes_router

# --- FastAPI Application Setup for backend to connect ---

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

# --- Routers ---

app.include_router(auth_router)
app.include_router(recipes_router)

# --- Routes for main ---

@app.get("/")
async def root():
    return {"message": "This is working"}