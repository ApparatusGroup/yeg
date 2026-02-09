# YEG Shadow Inventory — Technical Build Outline

**Version:** 1.0  
**Author:** Solutions Architecture  
**Target:** Codex / Coding Agent Handoff  
**Date:** 2026-02-09  

---

## Executive Summary

Build a stealth-tier local commerce concierge for Edmonton that aggregates real-time product data from independent shops into a single, seamless search interface. The system must feel **invisible** — no chatbot chrome, no AI disclosure. Users experience a direct line to every shelf in the city.

---

## Tech Stack Overview

| Layer | Technology | Rationale |
|---|---|---|
| Crawler / Fingerprinter | Python 3.12 + `httpx` + `BeautifulSoup4` | Async HTTP, fast HTML parsing |
| Extraction Engine | Python + `httpx` + `selectolax` | High-perf scraping with rate control |
| Data Enrichment (LLM) | Claude Haiku 4.5 via Anthropic API | Low-cost, fast categorization |
| Embeddings | `voyage-3-large` or `text-embedding-3-small` | High-quality semantic vectors |
| Vector Database | Supabase (pgvector) | Postgres-native, self-hostable, free tier |
| Backend API | FastAPI (Python 3.12) | Async, auto-docs, Pydantic validation |
| Frontend | Next.js 14 (App Router) + Tailwind CSS | SSR, ISR, edge-ready |
| Task Queue | Celery + Redis | Scheduled scraping, retry logic |
| Database (relational) | Supabase Postgres | Single platform for relational + vector |
| Deployment | Vercel (frontend) + Railway/Fly.io (API + workers) | Low-ops, auto-scaling |

---

## Implementation Order (Step-by-Step for Coding Agent)

```
Phase 1: Foundation          (Week 1–2)
  └─ Step 1: Project scaffolding & repo structure
  └─ Step 2: Database schema (Supabase Postgres + pgvector)
  └─ Step 3: Discovery & Fingerprinting Module

Phase 2: Data Pipeline       (Week 3–4)
  └─ Step 4: Extraction Engine — Shopify stores
  └─ Step 5: Extraction Engine — WooCommerce & Square
  └─ Step 6: Celery worker setup + scheduling

Phase 3: Intelligence        (Week 5–6)
  └─ Step 7: Data Enrichment & YEG Vibe Layer
  └─ Step 8: Embedding generation + vector indexing

Phase 4: API & Frontend      (Week 7–8)
  └─ Step 9: FastAPI backend + semantic search endpoint
  └─ Step 10: Next.js frontend — search bar + product grid
  └─ Step 11: "Where to Buy" / delivery CTA integration

Phase 5: Hardening           (Week 9–10)
  └─ Step 12: Monitoring, alerting, error handling
  └─ Step 13: Performance tuning + caching layer
  └─ Step 14: Store owner opt-in portal (v1.1)
```

---

## Project Structure

```
yeg-shadow-inventory/
├── backend/
│   ├── api/
│   │   ├── main.py                 # FastAPI app entrypoint
│   │   ├── routers/
│   │   │   ├── search.py           # /search endpoint
│   │   │   ├── products.py         # /products CRUD
│   │   │   └── stores.py           # /stores metadata
│   │   ├── models/
│   │   │   ├── product.py          # Pydantic models
│   │   │   ├── store.py
│   │   │   └── search.py
│   │   ├── services/
│   │   │   ├── semantic_search.py  # Vector search logic
│   │   │   ├── enrichment.py       # LLM enrichment calls
│   │   │   └── embedding.py        # Embedding generation
│   │   └── db/
│   │       ├── connection.py       # Supabase client
│   │       ├── schema.sql          # DDL + pgvector setup
│   │       └── queries.py          # Raw SQL helpers
│   ├── crawler/
│   │   ├── fingerprint.py          # Module 1: Discovery
│   │   ├── extractors/
│   │   │   ├── base.py             # Abstract extractor
│   │   │   ├── shopify.py          # Shopify /products.json
│   │   │   ├── woocommerce.py      # WooCommerce REST/sitemap
│   │   │   └── square.py           # Square catalog
│   │   ├── stealth.py              # UA rotation, rate limiting
│   │   └── scheduler.py            # Celery task definitions
│   ├── enrichment/
│   │   ├── categorizer.py          # LLM neighborhood/vibe tagging
│   │   ├── embedder.py             # Batch embedding pipeline
│   │   └── prompts.py              # Prompt templates
│   ├── config.py                   # Env vars, constants
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── app/
│   │   ├── page.tsx                # Landing — search bar
│   │   ├── search/
│   │   │   └── page.tsx            # Search results grid
│   │   ├── product/
│   │   │   └── [id]/page.tsx       # Product detail
│   │   └── layout.tsx
│   ├── components/
│   │   ├── SearchBar.tsx
│   │   ├── ProductCard.tsx
│   │   ├── ProductGrid.tsx
│   │   ├── NeighborhoodFilter.tsx
│   │   └── VibeTag.tsx
│   ├── lib/
│   │   └── api.ts                  # API client
│   ├── tailwind.config.ts
│   ├── next.config.js
│   └── package.json
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Module 1: Discovery & Fingerprinting

**File:** `backend/crawler/fingerprint.py`

### Objective
Given a CSV/JSON list of Edmonton shop URLs, detect the e-commerce backend powering each site. Prioritize Shopify stores for immediate extraction.

### Detection Logic

```
For each URL:
  1. GET the homepage with a browser-like User-Agent
  2. Run detection heuristics (order = priority):

     SHOPIFY signals:
       - Response header: "x-shopify-stage" or "x-shopid"
       - <meta name="shopify-*"> tags in HTML
       - Presence of cdn.shopify.com in page source
       - GET /products.json returns 200

     WOOCOMMERCE signals:
       - <meta name="generator" content="WooCommerce ...">
       - /wp-json/wc/v3/ endpoint responds
       - "woocommerce" class in <body> tag
       - /wp-content/plugins/woocommerce/ in source

     SQUARE signals:
       - "squarespace" in source (differentiate from Square Online)
       - square.site domain
       - "square" meta tags
       - /s/shop or /store path patterns

     UNKNOWN:
       - None of the above → flag for manual review
  
  3. Write result to `stores` table with:
     - url, platform, confidence_score, detected_at
```

### Python Libraries

```
httpx                   # Async HTTP client
beautifulsoup4          # HTML parsing
selectolax              # Fast CSS selector parsing (fallback)
tldextract              # Domain extraction
```

### Key Implementation Notes for Coding Agent

- Use `httpx.AsyncClient` with connection pooling (max 10 concurrent).
- Set a 10-second timeout per request.
- Store raw detection signals as JSONB for audit trail.
- Output: A `stores` table row with `platform` enum: `shopify | woocommerce | square | unknown`.

---

## Module 2: Extraction Engine ("Stealth Scraper")

**Files:** `backend/crawler/extractors/`, `backend/crawler/stealth.py`

### 2A: Shopify Extractor

**Endpoint:** `https://{domain}/products.json?limit=250&page={n}`

```
Loop pages until empty:
  For each product in response["products"]:
    Extract:
      - title:            product["title"]
      - description:      strip_html(product["body_html"])
      - vendor:           product["vendor"]
      - product_type:     product["product_type"]
      - tags:             product["tags"]  (comma-separated string)
      - created_at:       product["created_at"]
      - updated_at:       product["updated_at"]  → "Last Updated"
      - images:           [v["src"] for v in product["images"]]
      - For each variant in product["variants"]:
          - price:        variant["price"]
          - compare_price: variant["compare_at_price"]
          - sku:          variant["sku"]
          - available:    variant["available"]  → Inventory Status
          - option_title: variant["title"]
```

**Pagination:** Shopify limits to 250 products/page. Paginate until `products` array is empty.

### 2B: WooCommerce Extractor

**Primary:** WooCommerce REST API (if public): `GET /wp-json/wc/v3/products?per_page=100`  
**Fallback:** Parse `/sitemap_index.xml` → find product sitemap → crawl each product URL → extract via structured data (`ld+json`) or CSS selectors.

```
Structured data targets (ld+json, type="Product"):
  - name, description, image, offers.price,
    offers.availability, offers.priceCurrency
```

### 2C: Square Extractor

**Approach:** Square Online stores don't expose a public product API. Scrape the `/s/shop` or `/store` pages.

```
Strategy:
  1. GET store page
  2. Look for embedded JSON in <script> tags (Square often hydrates state)
  3. Fallback: CSS selectors for product cards
  4. Extract: title, price, image, availability
```

### 2D: Stealth / Polite Scraping Module

**File:** `backend/crawler/stealth.py`

```python
# Configuration constants
RATE_LIMIT_SECONDS = 2.0        # Min delay between requests to same domain
MAX_CONCURRENT_PER_DOMAIN = 2   # Max parallel requests per domain
GLOBAL_CONCURRENCY = 10         # Total parallel requests across all domains
RETRY_ATTEMPTS = 3
RETRY_BACKOFF = [5, 15, 60]     # Seconds

# User-Agent rotation pool (real browser strings, update quarterly)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ...",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 ...",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ...",
    # ... 15-20 agents
]
```

**Rules:**
1. **Respect `robots.txt`** — parse and obey before crawling. Use `robotsparser` library.
2. **Rate limit per domain** — enforce via `asyncio.Semaphore` per domain + `asyncio.sleep`.
3. **Rotate User-Agent** — random selection per request from pool.
4. **Exponential backoff on 429/503** — wait and retry with increasing delay.
5. **No session persistence** — each request gets a fresh set of headers.
6. **Honor `Retry-After` headers** — if present, use the server's requested delay.

### Python Libraries

```
httpx                   # Async HTTP with HTTP/2
beautifulsoup4          # HTML parsing
selectolax              # Fast HTML parsing (Shopify JSON doesn't need this)
bleach                  # HTML stripping from descriptions
robotsparser            # robots.txt compliance
tenacity                # Retry logic with backoff
asyncio                 # Concurrency control
```

### Data Schema (Products Table)

```sql
CREATE TABLE products (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    store_id        UUID REFERENCES stores(id) ON DELETE CASCADE,
    external_id     TEXT,                          -- Platform-specific ID
    title           TEXT NOT NULL,
    description     TEXT,
    description_raw TEXT,                          -- Original HTML
    price           DECIMAL(10,2),
    compare_price   DECIMAL(10,2),
    currency        TEXT DEFAULT 'CAD',
    images          TEXT[],                        -- Array of URLs
    sku             TEXT,
    available       BOOLEAN DEFAULT true,
    tags            TEXT[],
    product_type    TEXT,
    vendor          TEXT,
    source_url      TEXT,
    -- Enrichment fields (populated by Module 3)
    neighborhood    TEXT,
    vibe_tags       TEXT[],
    yeg_categories  TEXT[],
    -- Embedding (populated by Module 4)
    embedding       vector(1536),
    -- Metadata
    platform_updated_at TIMESTAMPTZ,               -- "Last Updated" from source
    first_seen_at   TIMESTAMPTZ DEFAULT now(),
    last_scraped_at TIMESTAMPTZ DEFAULT now(),
    is_active       BOOLEAN DEFAULT true,
    UNIQUE(store_id, external_id)
);

CREATE TABLE stores (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            TEXT,
    url             TEXT UNIQUE NOT NULL,
    platform        TEXT CHECK (platform IN ('shopify','woocommerce','square','unknown')),
    neighborhood    TEXT,
    address         TEXT,
    lat             DECIMAL(9,6),
    lng             DECIMAL(9,6),
    detection_meta  JSONB,
    is_active       BOOLEAN DEFAULT true,
    created_at      TIMESTAMPTZ DEFAULT now(),
    last_crawled_at TIMESTAMPTZ
);

-- Vector index for semantic search
CREATE INDEX ON products
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

-- Full-text search index (fallback/hybrid)
CREATE INDEX idx_products_fts ON products
    USING GIN (to_tsvector('english', title || ' ' || COALESCE(description, '')));
```

---

## Module 3: Data Enrichment & "YEG Vibe" Layer

**Files:** `backend/enrichment/categorizer.py`, `backend/enrichment/prompts.py`

### Pipeline Flow

```
Raw Product Record
  │
  ▼
┌──────────────────────────────────────┐
│  Step 1: Neighborhood Assignment     │
│  (from store address / postal code)  │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│  Step 2: LLM Categorization         │
│  (Claude Haiku 4.5 via Anthropic    │
│   API — batch processing)           │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│  Step 3: Vibe Tag Assignment         │
│  (Deterministic + LLM hybrid)       │
└──────────────┬───────────────────────┘
               │
               ▼
  Enriched Product Record → DB Update
```

### Step 1: Neighborhood Mapping

Maintain a lookup table mapping Edmonton postal code prefixes and known addresses to neighborhoods.

```python
EDMONTON_NEIGHBORHOODS = [
    "Old Strathcona", "Whyte Ave", "Ritchie", "Oliver", "Garneau",
    "Downtown", "124th Street", "Highlands", "Alberta Avenue",
    "Westmount", "Bonnie Doon", "Mill Woods", "Jasper Avenue",
    "Sherwood Park", "St. Albert", "Ice District", "Ellerslie",
    "Windermere", "Summerside", "The Quarters"
]
```

If the store record has a physical address, geocode it (Google Maps API or Nominatim) and map to the nearest neighborhood polygon. If no address, assign based on store website "About" / "Contact" page (scraped during fingerprinting).

### Step 2: LLM Categorization Prompt

**Model:** `claude-haiku-4-5-20251001` (via Anthropic API)  
**Batch size:** 20 products per request  
**Max tokens:** ~800 per batch

```python
CATEGORIZATION_PROMPT = """You are a product categorization engine for Edmonton, Alberta.

Given the following products, assign each one:
1. A primary "YEG Vibe" category from this list:
   - Winter-Proof (cold weather gear, insulation, warmth)
   - Festival Season (K-Days, Fringe, Heritage Days, Folk Fest essentials)
   - River Valley Ready (hiking, biking, trail gear, outdoor recreation)
   - Local Craft (handmade, artisan, locally produced)
   - YEG Gift (items that represent Edmonton identity)
   - Date Night (dining accessories, fashion, experiences)
   - Student Life (university essentials, budget-friendly)
   - Game Day (Oilers, Elks, FC Edmonton fan gear and tailgate)
   - Home on the Prairies (home decor, cozy, prairie aesthetic)
   - Market Fresh (food, beverage, local consumables)

2. Up to 3 secondary vibe tags (can overlap or be more specific)

3. A one-sentence "Local Pitch" — why an Edmontonian would want this.

Respond ONLY in JSON. No preamble.

Products:
{products_json}

Response format:
[
  {
    "product_id": "...",
    "primary_vibe": "...",
    "secondary_vibes": ["...", "..."],
    "local_pitch": "..."
  }
]"""
```

### Step 3: Deterministic Vibe Tags

Before/after LLM processing, apply rule-based tags for high-confidence patterns:

```python
VIBE_RULES = {
    r"(?i)(toque|parka|thermal|fleece|heated|insulated)": "Winter-Proof",
    r"(?i)(oilers|elks|oil kings|fc edmonton)": "Game Day",
    r"(?i)(honey|preserve|jam|bake|roast|coffee)": "Market Fresh",
    r"(?i)(handmade|hand-crafted|artisan|small.?batch)": "Local Craft",
    r"(?i)(yeg|edmonton|780|alberta)": "YEG Gift",
}
```

### Python Libraries

```
anthropic               # Anthropic Python SDK (Claude API)
geopy                   # Geocoding (Nominatim fallback)
```

---

## Module 4: Semantic Search Architecture

**Files:** `backend/api/services/semantic_search.py`, `backend/enrichment/embedder.py`

### Embedding Strategy

**Model:** OpenAI `text-embedding-3-small` (1536 dims) or Voyage `voyage-3-large`  
**What gets embedded:** A composite text field per product:

```python
def build_embedding_text(product: dict) -> str:
    parts = [
        product["title"],
        product.get("description", ""),
        product.get("vendor", ""),
        product.get("product_type", ""),
        f"Neighborhood: {product.get('neighborhood', 'Edmonton')}",
        f"Vibes: {', '.join(product.get('vibe_tags', []))}",
        product.get("local_pitch", ""),
    ]
    return " | ".join(filter(None, parts))
```

### Vector Storage (pgvector in Supabase)

Already defined in the schema above. Key operations:

```sql
-- Semantic search: find top N products by cosine similarity
SELECT id, title, price, images, neighborhood, vibe_tags,
       1 - (embedding <=> $1::vector) AS similarity
FROM products
WHERE is_active = true
ORDER BY embedding <=> $1::vector
LIMIT 20;
```

### Hybrid Search (Semantic + Full-Text + Filters)

```sql
-- Hybrid query: combine vector similarity with keyword boost and filters
WITH semantic AS (
    SELECT id, 1 - (embedding <=> $1::vector) AS vec_score
    FROM products
    WHERE is_active = true
    ORDER BY embedding <=> $1::vector
    LIMIT 100
),
keyword AS (
    SELECT id, ts_rank(
        to_tsvector('english', title || ' ' || COALESCE(description, '')),
        plainto_tsquery('english', $2)
    ) AS text_score
    FROM products
    WHERE is_active = true
      AND to_tsvector('english', title || ' ' || COALESCE(description, ''))
          @@ plainto_tsquery('english', $2)
)
SELECT p.*, 
       COALESCE(s.vec_score, 0) * 0.7 + COALESCE(k.text_score, 0) * 0.3 AS final_score
FROM products p
LEFT JOIN semantic s ON p.id = s.id
LEFT JOIN keyword k ON p.id = k.id
WHERE (s.id IS NOT NULL OR k.id IS NOT NULL)
  AND ($3::text IS NULL OR p.neighborhood = $3)
  AND ($4::text IS NULL OR $4 = ANY(p.vibe_tags))
ORDER BY final_score DESC
LIMIT 20;
```

### Embedding Pipeline

```
New/Updated Product
  │
  ▼
Build composite text → Generate embedding (API call) → UPDATE products SET embedding = ...
```

**Batch processing:** Embed in batches of 100. Run as a Celery task after each scrape cycle.

### Python Libraries

```
openai                  # For text-embedding-3-small (or voyageai for Voyage)
pgvector                # pgvector Python bindings for Supabase
numpy                   # Vector operations if needed
```

---

## Module 5: The "Invisible" API & Frontend

### 5A: FastAPI Backend

**File:** `backend/api/main.py`

#### Endpoints

```
GET  /api/v1/search?q={query}&neighborhood={n}&vibe={v}&page={p}&limit={l}
     → Hybrid semantic + keyword search
     → Returns: { results: Product[], total: int, facets: {} }

GET  /api/v1/products/{id}
     → Full product detail with store info
     → Returns: Product with store metadata

GET  /api/v1/products/{id}/similar
     → Vector-nearest products (exclude same store)
     → Returns: Product[]

GET  /api/v1/neighborhoods
     → List neighborhoods with product counts
     → Returns: { neighborhoods: [{ name, count }] }

GET  /api/v1/vibes
     → List vibe tags with product counts
     → Returns: { vibes: [{ name, count }] }

GET  /api/v1/trending
     → Recently added / frequently searched products
     → Returns: Product[]
```

#### Search Flow (Pseudocode)

```python
@router.get("/search")
async def search(q: str, neighborhood: str = None, vibe: str = None,
                 page: int = 1, limit: int = 20):
    # 1. Generate embedding for user query
    query_embedding = await generate_embedding(q)

    # 2. Run hybrid search (vector + full-text)
    results = await hybrid_search(
        embedding=query_embedding,
        keyword=q,
        neighborhood=neighborhood,
        vibe=vibe,
        offset=(page - 1) * limit,
        limit=limit
    )

    # 3. Return with facets for filtering UI
    facets = await get_facets(query_embedding, q)

    return {
        "results": results,
        "total": len(results),
        "facets": facets,
        "page": page
    }
```

#### Middleware & Config

```python
# CORS — allow frontend origin only
# Response caching — 60s TTL on search results (Redis)
# Rate limiting — 60 req/min per IP (slowapi)
# Request logging — structured JSON logs
```

### 5B: Next.js Frontend

#### UI/UX Directive (Critical for Coding Agent)

```
DO:
  ✓ Single search bar, centered, prominent — think "Google circa 2005" simplicity
  ✓ Instant results as you type (debounced 300ms)
  ✓ Product grid: image-forward cards (no text walls)
  ✓ Each card shows: Image, Title, Price, Store Name, Neighborhood badge
  ✓ Subtle vibe tag chips below each product (muted colors, not flashy)
  ✓ "Where to Buy" button → links to store product page (outbound link)
  ✓ "Instant Local Delivery" badge if store supports delivery (future: integrate with local couriers)
  ✓ Neighborhood filter as horizontal scrolling pills
  ✓ Vibe filter as toggleable chips
  ✓ Skeleton loading states (no spinners)
  ✓ Dark mode support
  ✓ Mobile-first responsive design

DO NOT:
  ✗ No chatbot widget
  ✗ No "Powered by AI" or "AI-generated" labels ANYWHERE
  ✗ No onboarding modals
  ✗ No login/signup (v1 is fully public)
  ✗ No "Hi, how can I help you?" — this is a search engine, not a conversation
  ✗ No infinite scroll — use pagination with "Load More" button
  ✗ No cookie banners (don't track users in v1)
```

#### Key Components

```
SearchBar.tsx
  - Full-width on landing, collapses to header on results page
  - Placeholder text rotates: "Find local honey...", "Winter boots from Whyte Ave...",
    "A gift that feels like Edmonton..."
  - Debounced search with AbortController for stale requests

ProductCard.tsx
  - Aspect ratio: 4:5 image container
  - Lazy-loaded images with blur placeholder
  - Price in bold, store name in muted text
  - Neighborhood pill badge (color-coded)
  - Hover: subtle lift + "View at {store_name}" overlay

ProductGrid.tsx
  - CSS Grid: 2 cols mobile, 3 cols tablet, 4 cols desktop
  - Masonry-style if image heights vary (use CSS columns or next/image)

NeighborhoodFilter.tsx
  - Horizontal scrollable pills
  - Shows count badge: "Ritchie (47)"
  - Multi-select with "All" default

VibeTag.tsx
  - Chip component with icon + label
  - Each vibe has a consistent color:
    Winter-Proof → Ice blue
    Festival Season → Warm orange
    River Valley Ready → Forest green
    Local Craft → Terracotta
    YEG Gift → Edmonton blue (#00205B)
```

#### Frontend Libraries

```
next@14                 # React framework
tailwindcss             # Utility-first CSS
@tanstack/react-query   # Data fetching + caching
framer-motion           # Subtle animations (card hover, page transitions)
nuqs                    # URL state management for search params
sharp                   # Image optimization (server-side)
```

---

## Scheduling & Orchestration

### Celery Task Schedule

```python
# celerybeat_schedule
CELERY_BEAT_SCHEDULE = {
    "full-crawl-shopify": {
        "task": "crawler.tasks.crawl_shopify_stores",
        "schedule": crontab(hour="*/6"),          # Every 6 hours
    },
    "full-crawl-woocommerce": {
        "task": "crawler.tasks.crawl_woocommerce_stores",
        "schedule": crontab(hour="*/12"),         # Every 12 hours
    },
    "enrichment-pipeline": {
        "task": "enrichment.tasks.enrich_new_products",
        "schedule": crontab(minute="*/30"),       # Every 30 min (new products only)
    },
    "embedding-sync": {
        "task": "enrichment.tasks.generate_embeddings",
        "schedule": crontab(minute="*/30"),       # Follows enrichment
    },
    "stale-product-check": {
        "task": "crawler.tasks.deactivate_stale",
        "schedule": crontab(hour=3, minute=0),    # Daily at 3 AM MST
    },
    "fingerprint-new-stores": {
        "task": "crawler.tasks.fingerprint_queue",
        "schedule": crontab(hour=2, minute=0),    # Daily at 2 AM MST
    },
}
```

### Staleness Logic

If a product hasn't been seen in 3 consecutive crawl cycles, set `is_active = false`. If a store returns 5xx for 3 consecutive crawl cycles, flag for manual review.

---

## Environment Variables

```bash
# .env.example
DATABASE_URL=postgresql://user:pass@host:5432/yeg_shadow
REDIS_URL=redis://localhost:6379/0

# APIs
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...              # For embeddings (or VOYAGE_API_KEY)

# Crawling
CRAWL_RATE_LIMIT=2.0               # Seconds between requests per domain
CRAWL_MAX_CONCURRENT=10
CRAWL_USER_AGENTS_FILE=config/user_agents.txt

# Frontend
NEXT_PUBLIC_API_URL=https://api.yegshadow.com
NEXT_PUBLIC_SITE_URL=https://yegshadow.com
```

---

## Requirements Files

### `backend/requirements.txt`

```
# Core
fastapi>=0.115.0
uvicorn[standard]>=0.30.0
pydantic>=2.9.0

# Database
supabase>=2.0.0
pgvector>=0.3.0
asyncpg>=0.30.0
sqlalchemy>=2.0.0

# Crawling
httpx[http2]>=0.27.0
beautifulsoup4>=4.12.0
selectolax>=0.3.0
bleach>=6.0.0
robotsparser>=0.1.0
tenacity>=9.0.0
tldextract>=5.0.0

# AI / ML
anthropic>=0.40.0
openai>=1.50.0                    # For embeddings
numpy>=1.26.0

# Task Queue
celery[redis]>=5.4.0
redis>=5.0.0

# Geocoding
geopy>=2.4.0

# Utilities
python-dotenv>=1.0.0
structlog>=24.0.0                 # Structured logging
slowapi>=0.1.9                    # Rate limiting
orjson>=3.10.0                    # Fast JSON
```

### `frontend/package.json` (key dependencies)

```json
{
  "dependencies": {
    "next": "^14.2.0",
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "@tanstack/react-query": "^5.60.0",
    "nuqs": "^2.0.0",
    "framer-motion": "^11.0.0"
  },
  "devDependencies": {
    "tailwindcss": "^3.4.0",
    "typescript": "^5.5.0",
    "@types/react": "^18.3.0",
    "eslint": "^8.57.0",
    "eslint-config-next": "^14.2.0"
  }
}
```

---

## Ethical & Legal Notes for Coding Agent

1. **robots.txt compliance is mandatory** — never scrape endpoints disallowed by robots.txt.
2. **Build an opt-out mechanism** — any store owner who contacts us must be removable within 24 hours. Add an `opted_out` boolean to the `stores` table and exclude from all crawls and results.
3. **No price manipulation** — display prices exactly as scraped. Never alter, round, or editorialize pricing.
4. **Attribution** — always link back to the original store. The goal is to drive traffic TO local businesses, not away from them.
5. **Data retention** — purge raw HTML / response bodies after extraction. Store only structured product data.
6. **Rate limiting on our API** — protect stores from accidental DDoS if our frontend goes viral. 60 req/min per IP on our search endpoint.

---

## Success Metrics (For Product Validation)

| Metric | Target (v1 Launch) |
|---|---|
| Stores indexed | 50+ Edmonton independent shops |
| Products searchable | 5,000+ SKUs |
| Search latency (p95) | < 500ms |
| Crawl freshness | < 12 hours stale |
| Semantic search relevance | 80%+ of top-5 results rated "relevant" by test users |
| "Where to Buy" click-through | > 15% of search sessions |

---

*End of Technical Build Outline. Hand this file to the coding agent and begin with Phase 1, Step 1.*
