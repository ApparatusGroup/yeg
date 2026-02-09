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
