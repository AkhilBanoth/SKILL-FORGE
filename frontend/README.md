# SkillForge frontend (React + Vite + TypeScript)

Connected to the SKILLFORGE FastAPI backend.

    npm install
    npm run dev        # http://localhost:5173  (proxies /api -> localhost:8000)
    npm run build

Run the backend first: `uvicorn app.main:app --reload --port 8000`.
Production: set `VITE_API_URL` and enable CORS on the backend (see below).

First admin: register a user, then set `role='admin'` in the users table.

CORS (backend `app/main.py`, only needed when not using the dev proxy):

    from fastapi.middleware.cors import CORSMiddleware
    app.add_middleware(CORSMiddleware, allow_origins=["https://your-frontend"], allow_methods=["*"], allow_headers=["*"])
