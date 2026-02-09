# YEG Shadow Inventory

Monorepo scaffold for an Edmonton local-commerce inventory search platform.

## Project layout

- `backend/` FastAPI API, crawler, enrichment, SQL schema, and worker schedule scaffold.
- `frontend/` Next.js 14 app-router UI scaffold.
- `docker-compose.yml` local orchestration for API + frontend + Redis.

## Run locally

## 1) Backend

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

## 2) Frontend

```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:3000`.

## 3) Full stack with Docker Compose

```bash
cp .env.example .env
docker compose up --build
```

## Notes

- The search endpoint is currently scaffolded and returns an empty list until DB + embedding integration is completed.
- Shopify extraction is implemented as a starter (`/products.json`) while WooCommerce and Square extractors are placeholders.
- If package installs fail in a restricted network, configure your Python/npm registry access first, then rerun install.
