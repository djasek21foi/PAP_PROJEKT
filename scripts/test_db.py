from src.db.connection import get_conn, DB_PATH

def main():
    c = get_conn()

    rows = c.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        ORDER BY name;
    """).fetchall()

    print("DB:", DB_PATH)
    print("Tables:", [r["name"] for r in rows])

    # optional: broj redaka po tablici
    for name in [r["name"] for r in rows]:
        n = c.execute(f"SELECT COUNT(*) AS n FROM {name};").fetchone()["n"]
        print(f"- {name}: {n} rows")

    c.close()

if __name__ == "__main__":
    main()
