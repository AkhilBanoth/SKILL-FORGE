# SkillForge Deployment Checklist

## 1. Environment setup
- Copy `.env.example` to `.env`.
- Replace all placeholder values with real secrets and service URLs.
- Set `ENVIRONMENT=production` for deployment.
- Generate a cryptographically random `SECRET_KEY` of at least 32 characters; production startup rejects sample values.
- Replace the example PostgreSQL host and credentials with the managed database URL; SQLite is rejected in production.
- Set `GEMINI_API_KEY` only in the production environment if AI features are enabled.

## 2. Database readiness
- Provision PostgreSQL and ensure the configured database exists.
- Confirm `DATABASE_URL` matches the production database host and credentials.
- The app currently initializes tables with SQLAlchemy `create_all` during startup; introduce and run a migration tool before shipping schema changes that require controlled upgrades.
- Verify MongoDB connectivity if the app uses the Mongo-backed recommendations or analytics services.

## 3. Security hardening
- Restrict CORS to trusted frontend origins via `ALLOWED_ORIGINS`.
- Remove all sample values from `.env.example`; production startup rejects placeholder origins.
- Keep `.env` outside source control and only inject environment variables in deployment.
- Use admin-only access controls on privileged endpoints.
- Review JWT signing settings and rotate secrets on a schedule.

## 4. Runtime deployment
- Build and run the backend service with the production environment loaded.
- Start the frontend build or serve the production bundle from the configured host.
- Confirm the app health endpoint returns healthy status.
- Check logs for database connection, JWT, and AI-service errors.

## 5. Production verification
- Validate `/health` returns success.
- Test authentication and RBAC for admin/mentor/learner roles.
- Confirm create, update, and delete workflows are protected correctly.
- Verify AI fallback messaging works when no Gemini key is configured.

## 6. Rollback plan
- Keep the last known good build and environment snapshot.
- Revert to the previous image or release if DB connectivity or auth fails.
- Restore the prior `.env` values from the secure secret manager or backup store.
- Re-run smoke tests before reopening traffic.
