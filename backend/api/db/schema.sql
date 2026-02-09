create extension if not exists vector;

create table if not exists stores (
  id uuid primary key,
  name text not null,
  domain text unique not null,
  homepage_url text not null,
  platform text,
  neighborhood text,
  opted_out boolean not null default false,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists products (
  id uuid primary key,
  store_id uuid not null references stores(id),
  external_id text,
  title text not null,
  description text,
  brand text,
  category text,
  price numeric,
  currency text not null default 'CAD',
  image_url text,
  source_url text not null,
  neighborhood text,
  vibes text[] not null default '{}',
  embedding vector(1536),
  is_active boolean not null default true,
  last_seen_at timestamptz,
  missing_cycles int not null default 0,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists idx_products_store_id on products(store_id);
create index if not exists idx_products_active on products(is_active);
create index if not exists idx_products_embedding on products using ivfflat (embedding vector_cosine_ops);
