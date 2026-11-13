# SkillForge Backend Deployment Checklist

## 1. Environment Setup
- Copy `.env.example` to `.env`.
- Replace all placeholder values with actual configuration.
- Set `ENVIRONMENT=production`.
- Generate a secure `SECRET_KEY` of at least 32 characters.
- Configure the production PostgreSQL connection.
- Configure MongoDB connection details.
- Add `GEMINI_API_KEY` if AI features are enabled.

## 2. Database Readiness
- Provision PostgreSQL and verify connectivity.
- Confirm the production database URL.
- Verify MongoDB connectivity.
- Introduce and run database migrations before controlled schema changes.

## 3. Security
- Keep `.env` outside source control.
- Store production credentials securely.
- Verify JWT signing and expiration settings.
- Verify role-based access controls for admin, mentor, and learner.
- Protect privileged API endpoints.

## 4. Backend Deployment
- Install dependencies from `requirements.txt`.
- Start FastAPI using the production ASGI server.
- Verify the `/health` endpoint.
- Check logs for database, authentication, and AI-service errors.

## 5. Production Verification
- Test API documentation at `/docs`.
- Verify registration and login.
- Test authentication and authorization.
- Verify core learning, assessment, project, and certification APIs.
- Verify AI fallback behavior when Gemini is unavailable.

## 6. Rollback
- Keep the last known working deployment.
- Restore the previous configuration if deployment fails.
- Verify database connectivity and run smoke tests after rollback.