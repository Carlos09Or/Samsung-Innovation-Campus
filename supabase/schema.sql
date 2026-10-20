-- Mis cuadernos · esquema para Supabase
-- Pégalo completo en Supabase → SQL Editor → New query → Run.
-- Cada fila pertenece a un usuario y la seguridad a nivel de fila (RLS)
-- impide que otra cuenta la lea o la modifique.

create table if not exists public.carpetas (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  parent_id uuid references public.carpetas(id) on delete cascade,
  nombre text not null check (char_length(nombre) between 1 and 120),
  creado timestamptz not null default now()
);

create table if not exists public.cuadernos (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  carpeta_id uuid references public.carpetas(id) on delete set null,
  titulo text not null default 'Cuaderno sin título' check (char_length(titulo) <= 200),
  clase text,
  diapositivas jsonb not null default '[]'::jsonb,
  creado timestamptz not null default now(),
  actualizado timestamptz not null default now()
);

create index if not exists carpetas_user_idx on public.carpetas(user_id);
create index if not exists cuadernos_user_idx on public.cuadernos(user_id);

alter table public.carpetas enable row level security;
alter table public.cuadernos enable row level security;

drop policy if exists "carpetas propias" on public.carpetas;
create policy "carpetas propias" on public.carpetas
  for all to authenticated
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

drop policy if exists "cuadernos propios" on public.cuadernos;
create policy "cuadernos propios" on public.cuadernos
  for all to authenticated
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);
