# Launch Checklist

## Required Environment Settings

- Set `DJANGO_DEBUG=False`.
- Set a strong `DJANGO_SECRET_KEY`; production will not start without it.
- Set `DJANGO_ALLOWED_HOSTS` to the production domains and server IPs.
- Set `DJANGO_CSRF_TRUSTED_ORIGINS` to the HTTPS site origins.
- HTTPS settings default to enabled when `DJANGO_DEBUG=False`; override only when your proxy handles the same control:
  - `DJANGO_SECURE_SSL_REDIRECT=True`
  - `DJANGO_SESSION_COOKIE_SECURE=True`
  - `DJANGO_CSRF_COOKIE_SECURE=True`
  - `DJANGO_SECURE_HSTS_SECONDS=31536000`
  - `DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=True`
  - `DJANGO_SECURE_HSTS_PRELOAD=True`
- If behind a proxy or load balancer, set `DJANGO_USE_X_FORWARDED_PROTO=True`.
- Set `DJANGO_ADMIN_URL` to a private admin path, for example `staff-control/`.

## Before Opening to Users

- Run migrations.
- Run `python manage.py check --deploy`.
- Run `python manage.py collectstatic`.
- Confirm media uploads work in production.
- Confirm database backups are scheduled and tested.
- Confirm media file backups are scheduled and tested.
- Confirm backup restore has been tested on a separate machine or database.
- Confirm HTTPS works before enabling permanent HSTS settings.
- Create at least one superuser admin account.
- Add active publishing payment methods in Django admin.

## End-to-End Tests

- Register a new user with first and last name.
- Upload profile picture.
- Upload verification ID.
- Approve and reject verification from web admin and API.
- Confirm rejection reasons are visible to users/admins.
- Create a listing.
- Upload listing images.
- Submit payment reference.
- Approve and reject payment from web admin and API.
- Approve and reject listing from web admin and API.
- Confirm only paid, approved, available listings show publicly.
- Confirm 404, 403, and 500 pages render correctly.
