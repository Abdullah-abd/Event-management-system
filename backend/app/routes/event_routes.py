# app/routes/event_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import database, models, schemas, auth

router = APIRouter(prefix="/events", tags=["Events"])

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
# 🔴 Create new event (admin only)
# ---------------------------
@router.post("/", response_model=schemas.EventResponse)
def create_event(
    event: schemas.EventCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can add events")

    new_event = models.Event(**event.dict())
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event


# ---------------------------
# 🟠 Update event (admin only)
# ---------------------------
@router.put("/{event_id}", response_model=schemas.EventResponse)
def update_event(
    event_id: int,
    updated_data: schemas.EventUpdate,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can update events")

    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    update_dict = updated_data.dict(exclude_unset=True)

    # 🟢 Convert empty strings to None
    for key, value in list(update_dict.items()):
        if value == "":
            update_dict.pop(key)  # ⛔️ don’t overwrite with NULL

    for key, value in update_dict.items():
        setattr(event, key, value)

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
