GRANT ALL PRIVILEGES ON DATABASE db_main TO db_main;

\c db_main;

CREATE SCHEMA IF NOT EXISTS public;

CREATE TABLE public.atm (
        all_day BOOLEAN NOT NULL,
        services JSONB,
        id BIGSERIAL NOT NULL,
        internal_id UUID NOT NULL,
        address TEXT,
        coordinate geometry(POINT,4326),
        PRIMARY KEY (id),
        UNIQUE (internal_id)
);

CREATE TABLE public.offile (
        sale_point_name TEXT,
        individual_schedule JSONB NOT NULL,
        legal_entity_schedule JSONB NOT NULL,
        metro_station TEXT,
        my_branch BOOLEAN NOT NULL,
        kep BOOLEAN NOT NULL,
        has_ramp BOOLEAN NOT NULL,
        suo_availability BOOLEAN NOT NULL,
        sale_point_format TEXT,
        office_type TEXT,
        id BIGSERIAL NOT NULL,
        internal_id UUID NOT NULL,
        address TEXT,
        coordinate geometry(POINT,4326),
        PRIMARY KEY (id),
        UNIQUE (internal_id)
);

-- CREATE TABLE public.event(
--     id           bigserial
--         constraint event_pk
--             primary key,
--     created_at   timestamp with time zone not null,
--     exhauster_id int                      not null,
--     status       jsonb                    not null
-- );

-- CREATE UNIQUE INDEX on public.event (exhauster_id, created_at);
