from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query
from src.db import queries

app = FastAPI(
    title="PAP_PROJEKT API",
    version="0.1.0",
    description="REST API over SQLite database (pap.db)"
)

@app.get("/")
def root():
    return {"status": "ok", "endpoints": ["/tables", "/dt_yearly", "/wb_internet_year", "/integrated_individual"]}

@app.get("/tables")
def tables():
    return {"tables": queries.list_tables()}

@app.get("/dt_yearly")
def dt_yearly(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    return {"rows": queries.fetch_dt_yearly(limit=limit, offset=offset), "limit": limit, "offset": offset}

@app.get("/wb_internet_year")
def wb_internet_year(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    return {"rows": queries.fetch_wb_internet_year(limit=limit, offset=offset), "limit": limit, "offset": offset}

@app.get("/integrated_individual")
def integrated_individual(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    return {"rows": queries.fetch_integrated_individual(limit=limit, offset=offset), "limit": limit, "offset": offset}

@app.get("/table/{table_name}")
def any_table(
    table_name: str,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    try:
        rows = queries.fetch_all(table_name, limit=limit, offset=offset)
        return {"table": table_name, "rows": rows, "limit": limit, "offset": offset}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
