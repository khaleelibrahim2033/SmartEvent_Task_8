# SmartEvent API Endpoints

## Authentication
- POST `/api/auth/register`
- POST `/api/auth/login`
- GET `/api/auth/me`

## Events
- GET `/api/events/`
- GET `/api/events/categories`
- GET `/api/events/{event_id}`
- Public event responses include `event_status`: `UPCOMING`, `ONGOING`, `COMPLETED` or `CANCELLED`.

Query examples:
- `/api/events/?search=tech`
- `/api/events/?category=Music`

## Bookings (JWT required)
- POST `/api/bookings/`
- GET `/api/bookings/history`
- GET `/api/bookings/{booking_id}`

## Tickets
- GET `/api/tickets/`
- GET `/api/tickets/verify/{ticket_code}`

## Notifications (JWT required)
- GET `/api/notifications/`
- GET `/api/notifications/unread-count`
- PATCH `/api/notifications/{notification_id}/read`

## Organizer (ORGANIZER JWT required)
- POST `/api/organizer/events` — create an event owned by the current organizer
- GET `/api/organizer/events` — list owned events
- PATCH `/api/organizer/events/{event_id}` — update an owned event
- POST `/api/organizer/events/{event_id}/cancel` — cancel an owned event and notify attendees
- GET `/api/organizer/events/{event_id}/bookings` — list bookings for an owned event
- GET `/api/organizer/analytics` — per-event tickets, remaining capacity, revenue and booking counts

Organizer analytics accepts optional `start_date=YYYY-MM-DD` and `end_date=YYYY-MM-DD`.

## Administration (ADMIN JWT required)
- GET `/api/admin/users` — list users
- PATCH `/api/admin/users/{user_id}/role` — assign `USER`, `ORGANIZER` or `ADMIN`
- GET `/api/admin/events` — list all events
- GET `/api/admin/bookings` — list all bookings
- GET `/api/admin/analytics` — user/event totals, ticket and booking totals, revenue, daily sales,
  monthly trends, popular events and top revenue events

Admin analytics and bookings accept optional `start_date=YYYY-MM-DD` and `end_date=YYYY-MM-DD`.

New registrations are always `USER`. Provision the first administrator by setting `ADMIN_EMAIL`
and `ADMIN_PASSWORD` in `backend/.env` and running `python -m app.seed`.
