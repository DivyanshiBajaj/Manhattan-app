CREATE TABLE manhattan_neighborhood_populations (
    id                SERIAL PRIMARY KEY,
    borough           TEXT        NOT NULL,
    year              INTEGER     NOT NULL,
    fips_county_code  CHAR(3)     NOT NULL,
    nta_code          CHAR(4)     NOT NULL,
    nta_name          TEXT        NOT NULL,
    population        INTEGER     NOT NULL CHECK (population >= 0),
    UNIQUE (nta_code, year)
);
