# CITYMEMORY Prototype

This directory contains the current CITYMEMORY working prototype.

## Prototype scope

The prototype demonstrates a common asset/event model and six intelligence signals:

1. Infrastructure Amnesia
2. Failure Echo Mapper
3. Failure Signature Engine
4. Intervention Survival
5. Historical Intervention Comparison
6. Memory-Weighted Preventive Action Planner

The demo uses seeded sample data. It is a prototype demonstration and should not be interpreted as a live municipal deployment.

## Structure

- `frontend/` — React/Vite dashboard and map UI
- `backend/` — FastAPI API, data model, seed data and intelligence services

## Run locally

### Backend

From `prototype/backend/`:

```powershell
python -m pip install -r requirements.txt
python seed.py
uvicorn main:app --reload
```

By default the prototype can use its local SQLite configuration. For a PostgreSQL deployment, configure `DATABASE_URL` using `.env` based on `.env.example`.

### Frontend

From `prototype/frontend/`:

```powershell
npm install
npm run dev
```

The frontend expects the API at `http://127.0.0.1:8000` unless configured otherwise.
