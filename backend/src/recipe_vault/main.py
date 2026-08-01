from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db

# from routes.#### import router as ####_router

app = FastAPI()

init_db()

origins = []

# app.add_middleware(
#     pass
# )

# app.include_router(####_router, prefix="/####", tags=["####"])

@app.get("/")
def read_root():
    return ("Nothing here to talk about")

