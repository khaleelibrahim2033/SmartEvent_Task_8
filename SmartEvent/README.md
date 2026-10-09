# SmartEvent – Event Discovery, Ticket Booking & Management

Full-stack event platform using **FastAPI + React (Vite)**, with member, organizer and administrator roles.

## Modules
1. User Authentication – registration, login, bcrypt, JWT, protected routes, profile
2. Event Discovery – event listing, details, category filtering and search
3. Ticket Booking – booking, automatic total calculation, availability validation and history
4. QR Code Ticket System – unique ticket codes, QR generation and verification
5. Event Reminder Notifications – booking notifications, notification list, unread count and mark-as-read
6. Frontend UI – React pages, reusable navigation, Axios integration and protected routes
7. RBAC – database-backed USER / ORGANIZER / ADMIN roles enforced on protected APIs
8. Organizer event management – event creation, editing, cancellation, bookings and sales metrics
9. Admin dashboard – user/role management, event and booking overviews, revenue and platform analytics
10. Event lifecycle – UPCOMING / ONGOING / COMPLETED / CANCELLED status and attendee notifications

## Tech Stack
### Backend
- Python
- FastAPI
- SQLAlchemy
- SQLite by default / MySQL supported
- Pydantic
- JWT
- bcrypt
- qrcode

### Frontend
- React
- Vite
- Axios
- React Router

## Quick Start

### 1. Backend
```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Edit .env and set a unique SECRET_KEY (at least 32 characters).
# Optional: set ADMIN_EMAIL and ADMIN_PASSWORD before seeding to create the first admin.
python -m app.seed
python -m uvicorn main:app --reload
```

Swagger: http://127.0.0.1:8000/docs

### 2. Frontend
Open a second terminal:
```bash
cd frontend
npm install
copy .env.example .env
npm run dev
```

Frontend: http://localhost:5173

### Roles and first administrator
Public registration always creates a `USER`. To create the first administrator, set
`ADMIN_EMAIL` and `ADMIN_PASSWORD` in `backend/.env` before running `python -m app.seed`.
The seed command creates that administrator, or promotes the matching existing account.
An administrator can change user roles from the Admin Dashboard. A newly assigned role
should sign out and back in so the frontend and role-bearing token are refreshed; role
authorization is checked against the database on every request. Never use the example
secret or demo credentials in production.

## Main User Flow
Register → Login → Browse Events → Search/Filter → Event Details → Select Quantity → Book → Confirmation → QR Ticket → Booking History → Notifications

## Database
Tables:
- users
- events
- bookings
- tickets
- notifications

Relationships:
- One user → many bookings
- One event → many bookings
- One booking → one or more tickets
- One user → many notifications
- One organizer → many events

## Security
- Passwords are stored as bcrypt hashes, never plain text.
- JWT includes the user's role; protected APIs enforce the current database role.
- Organizer event writes and booking lists are restricted to the event owner.
- Admin analytics, platform lists and role changes are administrator-only.
- Booking history and tickets are restricted to the logged-in owner.
- Pydantic validates incoming API data.
- Secrets are loaded from `.env`.
- Startup adds Phase 2 columns to existing SQLite/MySQL tables when missing.

## Important note
This is a development/demo implementation. For production, use a strong secret key, HTTPS, a production database, secure cookie/token strategy, database migrations, rate limiting, and a real background job system for scheduled reminders.
