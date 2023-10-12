-- CREATE DATABASE db_main;

GRANT ALL PRIVILEGES ON DATABASE db_main TO db_main;

\c db_main;

CREATE SCHEMA IF NOT EXISTS public;

-- CREATE TABLE public.event(
--     id           bigserial
--         constraint event_pk
--             primary key,
--     created_at   timestamp with time zone not null,
--     exhauster_id int                      not null,
--     status       jsonb                    not null
-- );

-- CREATE UNIQUE INDEX on public.event (exhauster_id, created_at);
