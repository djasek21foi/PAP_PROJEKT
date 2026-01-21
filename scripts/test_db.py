from src.db.connection import get_conn, DB_PATH
c = get_conn()
rows = c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print("DB:", DB_PATH)
print("Tables:", rows)
c.close()
