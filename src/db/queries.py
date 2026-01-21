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

def fetch_summary() -> dict[str, Any]:
    """
    Basic aggregate stats over integrated_individual table.
    """
    conn = get_conn()
    try:
        row = conn.execute("""
            SELECT
              COUNT(*) as n,
              AVG(daily_social_media_time) as avg_social_media_time,
              AVG(perceived_productivity_score) as avg_perceived_prod,
              AVG(actual_productivity_score) as avg_actual_prod
            FROM integrated_individual;
        """).fetchone()
        return dict(row) if row else {}
    finally:
        conn.close()


def fetch_dt_vs_internet() -> list[dict[str, Any]]:
    """
    Join DT yearly minutes with WorldBank internet percentage by year.
    """
    conn = get_conn()
    try:
        rows = conn.execute("""
            SELECT
              d.Year AS year,
              d.daily_minutes,
              w.internet_pct
            FROM dt_yearly d
            LEFT JOIN wb_internet_year w
              ON w.Year = d.Year
            ORDER BY d.Year;
        """).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()
