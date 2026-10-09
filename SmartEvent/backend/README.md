# SmartEvent Backend

FastAPI backend for the SmartEvent Event Discovery & Ticket Booking System.

## Features
- User registration and login
- bcrypt password hashing
- JWT authentication
- User profile
- Event discovery, search and category filtering
- Ticket booking and availability validation
- Booking history
- QR ticket generation
- Ticket verification
- Booking notifications
- Unread notification count and mark-as-read

## Run
```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Set a unique SECRET_KEY of at least 32 characters in .env.
# Optionally set ADMIN_EMAIL and ADMIN_PASSWORD before seeding to provision an admin.
python -m app.seed
python -m uvicorn main:app --reload
```

Swagger: http://127.0.0.1:8000/docs

The default database is SQLite for easy setup. For MySQL, set DATABASE_URL in `.env`.

Public registration creates USER accounts only. An admin can promote accounts to ORGANIZER
or ADMIN through the admin API. Phase 2 endpoints are documented in `../docs/API_ENDPOINTS.md`.
Existing databases receive the role and event ownership/status columns at API startup.
