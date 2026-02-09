# YEG Shadow Inventory

Monorepo scaffold for an Edmonton local-commerce inventory search platform.

## Project layout

- `backend/` FastAPI API, crawler, enrichment, SQL schema, and worker schedule scaffold.
- `frontend/` Next.js 14 app-router UI scaffold.
- `docker-compose.yml` local orchestration for API + frontend + Redis.

## Local development

### 1) Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

Health check:

```bash
curl http://localhost:8000/health
```

### 2) Frontend

```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:3000`.

### 3) Full stack with Docker Compose

```bash
cp .env.example .env
docker compose up --build
```

## Vercel deployment (frontend)

Yes — you can deploy the **frontend** to Vercel now.

1. Push this repo to GitHub.
2. In Vercel, import the repo.
3. Set **Root Directory** to `frontend`.
4. Framework preset should be Next.js (or auto-detected).
5. Add environment variable:
   - `NEXT_PUBLIC_API_URL=https://<your-backend-domain>`
6. Deploy.

### Backend hosting for production API

Vercel is not ideal for this backend because this project includes long-running crawl/worker jobs (Celery + Redis). Host backend/workers on Railway/Fly/Render and point `NEXT_PUBLIC_API_URL` to that API.

## Current scaffold status

- `/search` is scaffolded and returns empty results until DB + embeddings are wired.
- Shopify extraction has a starter implementation (`/products.json`), while WooCommerce/Square are placeholders.
- If installs fail in restricted networks, configure Python/npm registry access and retry.


## Vercel troubleshooting

- **401 on preview URL**: your Vercel project likely has deployment protection enabled; this is expected until authenticated.
- **404 on `/`**: this usually means Vercel built the repo root instead of the `frontend` app. This repo now includes a root `vercel.json` that routes traffic to `frontend` so root deploys work.
- **404 on `/favicon.ico`**: favicon is now provided at `/favicon.svg` via metadata.


## Backend deployment setup

Backend is now ready to deploy as a standalone FastAPI web service.

### Option A: Render (recommended quick start)

This repo includes `render.yaml` configured for the backend service (`rootDir: backend`).

1. Create a new Render Blueprint from this repo.
2. Set secrets in Render:
   - `DATABASE_URL`
   - `REDIS_URL`
3. Set CORS origins:
   - `BACKEND_CORS_ORIGINS=https://<your-vercel-domain>`
4. Deploy and note your API URL.
5. In Vercel frontend project, set:
   - `NEXT_PUBLIC_API_URL=https://<your-render-api-domain>`

### Option B: Railway/Fly/other

`backend/Procfile` is included with a production start command:

```bash
uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

Use the same environment variables as above.

### Production sanity checks

After deploy, verify:

```bash
curl https://<api-domain>/
curl https://<api-domain>/health
```

Both should return status payloads.
