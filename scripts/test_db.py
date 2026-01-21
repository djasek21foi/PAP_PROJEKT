from src.db.connection import get_conn, DB_PATH

c = get_conn()
rows = c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;").fetchall()

print("DB:", DB_PATH)
print("Tables:", [r["name"] for r in rows])

c.close()
