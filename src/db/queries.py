import pandas as pd
from .connection import get_conn

def list_tables() -> list[str]:
    conn = get_conn()
    rows = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;").fetchall()
    conn.close()
    # sqlite3.Row -> dict-like
    return [r["name"] if hasattr(r, "keys") else r[0] for r in rows]

def get_dt_yearly() -> list[dict]:
    conn = get_conn()
    df = pd.read_sql_query("SELECT * FROM dt_yearly ORDER BY Year;", conn)
    conn.close()
    return df.to_dict(orient="records")

def get_wb_internet_year() -> list[dict]:
    conn = get_conn()
    df = pd.read_sql_query("SELECT * FROM wb_internet_year ORDER BY Year;", conn)
    conn.close()
    return df.to_dict(orient="records")

def get_integrated_individual(limit: int = 100) -> list[dict]:
    conn = get_conn()
    df = pd.read_sql_query("SELECT * FROM integrated_individual LIMIT ?;", conn, params=(limit,))
    conn.close()
    return df.to_dict(orient="records")
