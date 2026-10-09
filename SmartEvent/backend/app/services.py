import os
import uuid
import qrcode
from pathlib import Path
from datetime import date, datetime, time, timedelta, timezone
from app.models.booking import Booking
from app.models.event import Event
from app.models.notification import Notification
from app.models.ticket import Ticket

QR_DIR = Path(__file__).resolve().parent / "static" / "qr"
QR_DIR.mkdir(parents=True, exist_ok=True)

def create_ticket(db, booking):
    code = f"SME-{uuid.uuid4().hex[:12].upper()}"
    filename = f"{code}.png"
    filepath = QR_DIR / filename
    qr = qrcode.make(code)
    qr.save(filepath)
    base_url = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
    ticket = Ticket(
        booking_id=booking.id,
        ticket_code=code,
        qr_code_url=f"{base_url}/static/qr/{filename}",
    )
    db.add(ticket)
    return ticket


def event_lifecycle_status(event: Event, now: datetime | None = None) -> str:
    if event.event_status == "CANCELLED":
        return "CANCELLED"

    current = now or datetime.now(timezone.utc)
    event_date = event.event_date
    if event_date.tzinfo is None:
        event_date = event_date.replace(tzinfo=timezone.utc)
    else:
        event_date = event_date.astimezone(timezone.utc)

    if event_date.date() == current.date():
        return "ONGOING"
    if event_date > current:
        return "UPCOMING"
    return "COMPLETED"


def refresh_event_statuses(db, events: list[Event]) -> None:
    changed = False
    for event in events:
        status = event_lifecycle_status(event)
        if event.event_status != status:
            event.event_status = status
            changed = True
    if changed:
        db.commit()


def notify_event_attendees(db, event: Event, title: str, message: str) -> None:
    user_ids = (
        db.query(Booking.user_id)
        .filter(Booking.event_id == event.id)
        .distinct()
        .all()
    )
    for (user_id,) in user_ids:
        db.add(Notification(
            user_id=user_id,
            title=title,
            message=message,
            type="EVENT",
        ))


def booking_date_filters(query, start_date: date | None, end_date: date | None):
    if start_date:
        query = query.filter(
            Booking.created_at >= datetime.combine(start_date, time.min)
        )
    if end_date:
        query = query.filter(
            Booking.created_at < datetime.combine(end_date + timedelta(days=1), time.min)
        )
    return query
