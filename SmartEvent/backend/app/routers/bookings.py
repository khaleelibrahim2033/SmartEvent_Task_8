from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user, require_roles
from app.models.user import User
from app.models.event import Event
from app.models.booking import Booking
from app.models.notification import Notification
from app.schemas.booking import BookingCreate, BookingResponse
from app.services import create_ticket, event_lifecycle_status

router = APIRouter(prefix="/api/bookings", tags=["Bookings"])

@router.post("/", response_model=BookingResponse, status_code=201)
def create_booking(data: BookingCreate, db: Session = Depends(get_db), user: User = Depends(require_roles("USER"))):
    event = db.query(Event).filter(Event.id == data.event_id).first()
    if not event:
        raise HTTPException(404, "Event not found")

    event_status = event_lifecycle_status(event)
    if event_status != "UPCOMING":
        if event_status == "CANCELLED":
            raise HTTPException(400, "Cannot book a cancelled event")
        raise HTTPException(400, "Cannot book an event that has started or completed")
    if data.ticket_quantity > event.available_tickets:
        raise HTTPException(400, f"Only {event.available_tickets} tickets are available")

    total = Decimal(str(event.ticket_price)) * data.ticket_quantity
    booking = Booking(
        user_id=user.id,
        event_id=event.id,
        ticket_quantity=data.ticket_quantity,
        total_price=total,
        booking_status="CONFIRMED",
    )
    event.available_tickets -= data.ticket_quantity
    db.add(booking)
    db.flush()
    create_ticket(db, booking)
    db.add(Notification(
        user_id=user.id,
        title="Booking Confirmed",
        message=f"Your booking for '{event.title}' is confirmed.",
        type="BOOKING",
    ))
    db.commit()
    db.refresh(booking)
    return booking

@router.get("/history", response_model=list[BookingResponse])
def booking_history(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Booking).filter(Booking.user_id == user.id).order_by(Booking.created_at.desc()).all()

@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    booking = db.query(Booking).filter(Booking.id == booking_id, Booking.user_id == user.id).first()
    if not booking:
        raise HTTPException(404, "Booking not found")
    return booking
