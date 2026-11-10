import csv
import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "Manhattan_populations_by_neighborhood_20261109.csv"


def main() -> None:
    load_dotenv(ROOT / ".env")
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise SystemExit("DATABASE_URL is not set in .env")

    schema_sql = (ROOT / "schema.sql").read_text()

    with psycopg2.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS manhattan_neighborhood_populations")
            cur.execute(schema_sql)

            with CSV_PATH.open(newline="") as csv_file:
                rows = [
                    (
                        row["Borough"],
                        int(row["Year"]),
                        row["FIPS County Code"],
                        row["NTA Code"],
                        row["NTA Name"],
                        int(row["Population"].replace(",", "")),
                    )
                    for row in csv.DictReader(csv_file)
                ]

            cur.executemany(
                """
                INSERT INTO manhattan_neighborhood_populations
                    (borough, year, fips_county_code, nta_code, nta_name, population)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                rows,
            )

            cur.execute(
                """
                SELECT COUNT(*), SUM(population)
                FROM manhattan_neighborhood_populations
                """
            )
            row_count, population_sum = cur.fetchone()

    print(f"row count: {row_count}")
    print(f"population sum: {population_sum}")


if __name__ == "__main__":
    main()
