import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("world_population.db")

# --- Step 1: build the database if it doesn't exist ---
with sqlite3.connect(DB_PATH) as conn:
    cur = conn.cursor()

    # 1a. Create table (do this only once)
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS population (
            countryName TEXT,
            Year        INTEGER,
            Population  INTEGER
        );
        """
    )

    # 1b. Seed some sample rows (skip duplicates)
    sample_rows = [
        ("India",   2024, 1_420_000_000),
        ("USA",     2024,   340_000_000),
        ("Brazil",  2024,   215_000_000),
        ("Germany", 2024,    84_000_000),
        ("Japan",   2024,   124_000_000),
    ]
    cur.executemany(
        """
        INSERT OR IGNORE INTO population (countryName, Year, Population)
        VALUES (?,?,?);
        """,
        sample_rows,
    )
    conn.commit()

# --- Step 2: run your query and load into a DataFrame ---
query = """
    SELECT countryName, Population
    FROM   population
    WHERE  Year = 2024;
"""

with sqlite3.connect(DB_PATH) as conn:
    results = pd.read_sql_query(query, conn)

# --- Step 3: show the results ---
print("\n2024 World Population (sample):\n")
print(results.to_string(index=False))

