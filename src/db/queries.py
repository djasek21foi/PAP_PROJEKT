from __future__ import annotations
from typing import Any, Optional

from .connection import get_conn

def list_tables() -> list[str]:
    conn = get_conn()
    try:
        rows = conn.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            ORDER BY name;
        """).fetchall()
        return [r["name"] for r in rows]
    finally:
        conn.close()

def fetch_all(table: str, limit: int = 100, offset: int = 0) -> list[dict[str, Any]]:

    allowed = set(list_tables())
    if table not in allowed:
        raise ValueError(f"Unknown table: {table}")

    conn = get_conn()
    try:
        rows = conn.execute(
            f"SELECT * FROM {table} LIMIT ? OFFSET ?;",
            (limit, offset)
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

def fetch_dt_yearly(limit: int = 100, offset: int = 0):
    return fetch_all("dt_yearly", limit=limit, offset=offset)

def fetch_wb_internet_year(limit: int = 100, offset: int = 0):
    return fetch_all("wb_internet_year", limit=limit, offset=offset)

def fetch_integrated_individual(limit: int = 100, offset: int = 0):
    return fetch_all("integrated_individual", limit=limit, offset=offset)
