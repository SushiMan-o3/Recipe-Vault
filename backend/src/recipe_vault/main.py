from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config import FRONTEND_URL
from database import init_db
from routes import auth, user
from routes.user import UPLOAD_DIR

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
app.include_router(user.route)

# StaticFiles refuses to mount a directory that doesn't exist yet, and it won't
# on a fresh checkout since uploads/ is gitignored.
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount(
    "/static/profile-pictures",
    StaticFiles(directory=UPLOAD_DIR),
    name="profile-pictures",
)

@app.get("/")
def read_root():
    return ("Nothing here to talk about")

