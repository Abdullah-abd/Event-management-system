# app/routes/event_routes.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
from .. import database, models, schemas, auth
import os

router = APIRouter(prefix="/events", tags=["Events"])

# Directory to save uploaded images
IMAGE_DIR = "static/images"
os.makedirs(IMAGE_DIR, exist_ok=True)

# ---------------------------
# 🟢 Get all events (any user)
# ---------------------------
@router.get("/", response_model=list[schemas.EventResponse])
def get_events(db: Session = Depends(database.get_db)):
    return db.query(models.Event).all()


# ---------------------------
# 🟢 Get single event by id
# ---------------------------
@router.get("/{event_id}", response_model=schemas.EventResponse)
def get_event(event_id: int, db: Session = Depends(database.get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


# ---------------------------
# 🔴 Create new event (admin only) with optional image upload
# ---------------------------
@router.post("/", response_model=schemas.EventResponse)
async def create_event(
    title: str = Form(...),
    description: str = Form(...),
    date: str = Form(...),
    time: str = Form(...),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can add events")

    image_url = None
    if image:
        file_path = os.path.join(IMAGE_DIR, image.filename)
        with open(file_path, "wb") as f:
            f.write(await image.read())
        image_url = f"/{IMAGE_DIR}/{image.filename}"  # URL accessible

    new_event = models.Event(
        title=title,
        description=description,
        date=date,
        time=time,
        image_url=image_url
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event


# ---------------------------
# 🟠 Update event (admin only) with optional image upload
# ---------------------------
@router.put("/{event_id}", response_model=schemas.EventResponse)
async def update_event(
    event_id: int,
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can update events")

    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if title is not None:
        event.title = title
    if description is not None:
        event.description = description

    if image:
        file_path = os.path.join(IMAGE_DIR, image.filename)
        with open(file_path, "wb") as f:
            f.write(await image.read())
        event.image_url = f"/{IMAGE_DIR}/{image.filename}"

    db.commit()
    db.refresh(event)
    return event


# ---------------------------
# 🔴 Delete event (admin only)
# ---------------------------
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
