from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from sqlalchemy import text

from . import models
from .database import engine, get_db
from .routes import auth_routes  # ✅ import router
from .routes import event_routes

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Event Management System")
bearer_scheme = HTTPBearer()
app.include_router(auth_routes.router)  # ✅ add routes
app.include_router(event_routes.router) # ✅ add routes

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
