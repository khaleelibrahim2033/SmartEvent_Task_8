from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict

class BookingCreate(BaseModel):
    event_id: int
    ticket_quantity: int = Field(gt=0, le=20)

class BookingResponse(BaseModel):
    id: int
    user_id: int
    event_id: int
    ticket_quantity: int
    total_price: Decimal
    booking_status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
