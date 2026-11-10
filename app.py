import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from flask import Flask, render_template
from psycopg2.extras import RealDictCursor

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

app = Flask(__name__)


def format_commas(value):
    number = float(value)
    if number.is_integer():
        return f"{int(number):,}"
    return f"{number:,.1f}"


app.jinja_env.filters["commas"] = format_commas


def get_connection():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not set")
    return psycopg2.connect(database_url)


@app.route("/")
def index():
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT nta_name, population
                FROM manhattan_neighborhood_populations
                ORDER BY nta_name
                """
            )
            neighborhoods = cur.fetchall()

            cur.execute(
                """
                SELECT
                    COALESCE(SUM(population), 0) AS total_population,
                    COALESCE(AVG(population), 0) AS average_population
                FROM manhattan_neighborhood_populations
                """
            )
            summary = cur.fetchone()

    return render_template(
        "index.html",
        neighborhoods=neighborhoods,
        total_population=summary["total_population"],
        average_population=summary["average_population"],
    )


if __name__ == "__main__":
    app.run(debug=True)
