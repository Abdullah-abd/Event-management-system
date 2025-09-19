from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine, get_db
from .routes import auth_routes  # ✅ import router
from .routes import event_routes
import os
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Event Management System")
bearer_scheme = HTTPBearer()
app.include_router(auth_routes.router)  # ✅ add routes
app.include_router(event_routes.router) # ✅ add routes
# Allow your frontend origin
origins = [
    "http://localhost:3000",   # Next.js local dev
    "http://127.0.0.1:3000",
    "https://event-management-system-seven-mu.vercel.app/",  # Production domain (frontend)
]

# serve uploaded images

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,         # or ["*"] for all origins
    allow_credentials=True,
    allow_methods=["*"],           # allows GET, POST, PUT, DELETE, OPTIONS
    allow_headers=["*"],           # allows headers like Content-Type, Authorization
)
@app.get("/")
def root():
    return {"message": "Event Management Backend is running 🚀"}

@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "connected ✅"}
    except Exception as e:
        return {"status": "error ❌", "details": str(e)}
