import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import inspect, text

from app.database import Base, engine
from app.routers import admin, auth, bookings, events, notifications, organizer, tickets
Base.metadata.create_all(bind=engine)


def upgrade_phase_two_schema():
    inspector = inspect(engine)
    additions = {
        "users": {
            "role": "VARCHAR(20) NOT NULL DEFAULT 'USER'",
        },
        "events": {
            "organizer_id": "INTEGER",
            "event_status": "VARCHAR(20) NOT NULL DEFAULT 'UPCOMING'",
        },
    }
    with engine.begin() as connection:
        for table, columns in additions.items():
            existing = {column["name"] for column in inspector.get_columns(table)}
            for column, definition in columns.items():
                if column not in existing:
                    connection.execute(
                        text(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")
                    )


upgrade_phase_two_schema()

app = FastAPI(title="SmartEvent API", version="2.0.0")

frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("app/static/qr", exist_ok=True)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(auth.router)
app.include_router(events.router)
app.include_router(bookings.router)
app.include_router(tickets.router)
app.include_router(notifications.router)
app.include_router(organizer.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return {"message": "Welcome to SmartEvent API", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}
