from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models.user import User
from app.models.ticket import Ticket
from app.models.booking import Booking
from app.schemas.ticket import TicketResponse

router = APIRouter(prefix="/api/tickets", tags=["Tickets"])

@router.get("/", response_model=list[TicketResponse])
def my_tickets(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return (
        db.query(Ticket)
        .join(Booking, Ticket.booking_id == Booking.id)
        .filter(Booking.user_id == user.id)
        .order_by(Ticket.created_at.desc())
        .all()
    )

@router.get("/verify/{ticket_code}")
def verify_ticket(ticket_code: str, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.ticket_code == ticket_code).first()
    if not ticket:
        raise HTTPException(404, "Invalid ticket")
    return {
        "valid": True,
        "ticket_code": ticket.ticket_code,
        "booking_id": ticket.booking_id,
        "message": "Ticket verified successfully",
    }
