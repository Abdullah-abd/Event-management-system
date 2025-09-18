from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text   # ✅ add this

from . import models
from .database import engine, get_db

# Create database tables if not already present
models.Base.metadata.create_all(bind=engine)

# FastAPI instance
app = FastAPI(title="Event Management System")

@app.get("/")
def root():
    return {"message": "Event Management Backend is running 🚀"}

# ✅ DB connection check endpoint
@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))   # ✅ wrap in text()
        return {"status": "connected ✅"}
    except Exception as e:
        return {"status": "error ❌", "details": str(e)}
