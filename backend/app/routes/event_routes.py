# app/routes/event_routes.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from datetime import datetime
import os, shutil
from pathlib import Path
import uuid

from .. import database, models, schemas, auth

router = APIRouter(prefix="/events", tags=["Events"])
BASE_URL = "http://127.0.0.1:8000"

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------------------------
# Get all events
@router.get("/", response_model=list[schemas.EventResponse])
def get_events(db: Session = Depends(database.get_db)):
    events = db.query(models.Event).all()
    for e in events:
        if e.image_url and not e.image_url.startswith("http"):
            e.image_url = f"{BASE_URL}{e.image_url}"
    return events

# ---------------------------
# Get single event
@router.get("/{event_id}", response_model=schemas.EventResponse)
def get_event(event_id: int, db: Session = Depends(database.get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.image_url and not event.image_url.startswith("http"):
        event.image_url = f"{BASE_URL}{event.image_url}"
    return event

# ---------------------------
# Create new event (admin only)
# ---------------------------
# Create new event (admin only)
@router.post("/", response_model=schemas.EventResponse)
async def create_event(
    title: str = Form(...),
    description: str = Form(...),
    date: str = Form(...),
    time: str = Form(...),
    image_url: UploadFile = File(None),  # ✅ name matches frontend
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can add events")

    # Convert date/time
    try:
        event_date = datetime.strptime(date, "%Y-%m-%d").date()
        event_time = datetime.strptime(time, "%H:%M").time()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date or time format")

    # Handle image upload
    image_path = None
    if image_url:
        ext = Path(image_url.filename).suffix
        safe_filename = f"{uuid.uuid4()}{ext}"
        file_path = os.path.join(UPLOAD_DIR, safe_filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image_url.file, buffer)
        image_path = f"/uploads/{safe_filename}"

    new_event = models.Event(
        title=title,
        description=description,
        date=event_date,
        time=event_time,
        image_url=image_path
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    # Add BASE_URL for response
    if new_event.image_url and not new_event.image_url.startswith("http"):
        new_event.image_url = f"{BASE_URL}{new_event.image_url}"

    return new_event

# ---------------------------
# Update event (admin only)
@router.put("/{event_id}", response_model=schemas.EventResponse)
async def update_event(
    event_id: int,
    title: str = Form(None),
    description: str = Form(None),
    date: str = Form(None),
    time: str = Form(None),
    image_url: UploadFile = File(None),  # ✅ name matches frontend
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can update events")

    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Update fields
    if title and title.strip():
        event.title = title
    if description and description.strip():
        event.description = description
    if date:
        try:
            event.date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format")
    if time:
        try:
            event.time = datetime.strptime(time, "%H:%M").time()
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid time format")

    # Handle image upload
    if image_url:
        ext = Path(image_url.filename).suffix
        safe_filename = f"{uuid.uuid4()}{ext}"
        file_path = os.path.join(UPLOAD_DIR, safe_filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image_url.file, buffer)
        event.image_url = f"/uploads/{safe_filename}"

    db.commit()
    db.refresh(event)

    if event.image_url and not event.image_url.startswith("http"):
        event.image_url = f"{BASE_URL}{event.image_url}"

    return event

# ---------------------------
# Delete event (admin only)
@router.delete("/{event_id}")
def delete_event(
    event_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can delete events")

    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    db.delete(event)
    db.commit()
    return {"message": "Event deleted successfully"}
