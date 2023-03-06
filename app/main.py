from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.api.chat import main as chat_router
from app.api.auth import main as auth_router
from app.db import engine, SessionLocal, Base

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize app
app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[""],
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router.router)
app.include_router(chat_router.router)

# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# HTML home
@app.get("/", response_class=HTMLResponse)
async def read_home():
    with open("app/static/home.html", "r") as f:
        html = f.read()
    return html
