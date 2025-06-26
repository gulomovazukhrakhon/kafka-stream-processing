CREATE TABLE IF NOT EXISTS telemtry_data (
    ts DOUBLE PRECISION,
    device TEXT,
    co DOUBLE PRECISION,
    humidity DOUBLE PRECISION,
    light BOOLEAN,
    lpg DOUBLE PRECISION,
    motion BOOLEAN,
    smoke DOUBLE PRECISION,
    temp DOUBLE PRECISION,
    PRIMARY KEY (ts, device)
);
