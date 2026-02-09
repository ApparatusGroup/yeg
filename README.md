# YEG Shadow Inventory

Monorepo scaffold for an Edmonton local-commerce inventory search platform.

## What's included

- **Backend (FastAPI)** with starter routers (`/search`, `/products`, `/stores`) and schema baseline.
- **Crawler foundation** with platform fingerprinting and extractor interface.
- **Enrichment stubs** for vibe classification and embedding hooks.
- **Frontend (Next.js 14)** with initial landing/search/detail pages and reusable components.
- **Docker Compose** for local API + frontend + Redis startup.

## Quick start

### 1) Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn api.main:app --reload
```

### 2) Frontend

```bash
cd frontend
npm install
npm run dev
```

### 3) Docker Compose

```bash
cp .env.example .env
docker compose up --build
```

## Current status

This commit delivers **Phase 1 foundation + project scaffolding** from the build outline.
Data persistence, real vector search, and live storefront extraction are intentionally scaffolded and ready for iterative implementation.
