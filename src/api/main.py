from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query, Path
from src.db import queries

app = FastAPI(
    title="Utjecaj online sadržaja na dnevne navike i produktivnost.",
    version="0.1.0",
    description=(
        "Napravio : David Jasek\n\n"
        "API za analizu utjecaja online sadržaja na dnevne navike i produktivnost.\n\n"
        "Pregled podataka iz različitih izvora (DT, WorldBank) i integrirani skup podataka na razini pojedinca.\n\n"
        "Tip: prvo pozovi /tables da vidiš dostupne tablice, "
        "zatim koristi /table/{table_name} "
    ),
)


@app.get(
    "/",
    tags=["info"],
    summary="Info + upute za testiranje",
    description=(
        "Brze upute:\n"
        "1) Otvori Swagger: /docs\n"
        "2) Klikni /tables da dobiješ popis tablica\n"
        "3) Testiraj /integrated_individual?limit=5\n"
        "4) Testiraj analitiku: /analytics/summary i /analytics/dt_vs_internet\n"
    ),
)
def root():
    return {
        "status": "ok",
        "how_to_test": [
            "Open Swagger UI: /docs",
            "GET /tables (list available tables)",
            "GET /integrated_individual?limit=5",
            "GET /analytics/summary",
            "GET /analytics/dt_vs_internet",
        ],
        "examples": {
            "tables": "/tables",
            "any_table_example": "/table/integrated_individual?limit=5&offset=0",
        },
        "docs": "/docs",
        "openapi": "/openapi.json",
    }



@app.get(
    "/tables",
    tags=["tables"],
    summary="Popis tablica u SQLite bazi",
    description="Vraća listu tablica dostupnih u pap.db (SQLite).",
)
def tables():
    return {"tables": queries.list_tables()}


@app.get(
    "/table/{table_name}",
    tags=["tables"],
    summary="Dohvati retke iz bilo koje tablice",
    description=(
        "Unesi naziv tablice (table_name) iz /tables.\n\n"
        "Primjer: table_name=integrated_individual, limit=5, offset=0"
    ),
)
def any_table(
    table_name: str = Path(
        ...,
        description="Naziv tablice (mora biti jedna od vrijednosti koje vrati /tables).",
        example="integrated_individual",
    ),
    limit: int = Query(
        100,
        ge=1,
        le=1000,
        description="Broj redaka za vratiti (paging).",
        example=50,
    ),
    offset: int = Query(
        0,
        ge=0,
        description="Pomak (paging). Npr. offset=50 za sljedeću stranicu.",
        example=0,
    ),
):
    try:
        rows = queries.fetch_all(table_name, limit=limit, offset=offset)
        return {"table": table_name, "rows": rows, "limit": limit, "offset": offset}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))



@app.get(
    "/dt_yearly",
    tags=["datasets"],
    summary="DT agregat po godinama",
    description="Dohvati tablicu dt_yearly (agregirani podaci po godini).",
)
def dt_yearly(
    limit: int = Query(100, ge=1, le=1000, description="Broj redaka", example=10),
    offset: int = Query(0, ge=0, description="Pomak", example=0),
):
    return {
        "rows": queries.fetch_dt_yearly(limit=limit, offset=offset),
        "limit": limit,
        "offset": offset,
    }


@app.get(
    "/wb_internet_year",
    tags=["datasets"],
    summary="WorldBank Internet % po godinama",
    description="Dohvati tablicu wb_internet_year (internet postotak po godini).",
)
def wb_internet_year(
    limit: int = Query(100, ge=1, le=1000, description="Broj redaka", example=10),
    offset: int = Query(0, ge=0, description="Pomak", example=0),
):
    return {
        "rows": queries.fetch_wb_internet_year(limit=limit, offset=offset),
        "limit": limit,
        "offset": offset,
    }


@app.get(
    "/integrated_individual",
    tags=["datasets"],
    summary="Integrirani individual-level skup",
    description="Dohvati tablicu integrated_individual (integrirani skup na razini pojedinca).",
)
def integrated_individual(
    limit: int = Query(100, ge=1, le=1000, description="Broj redaka", example=5),
    offset: int = Query(0, ge=0, description="Pomak", example=0),
):
    return {
        "rows": queries.fetch_integrated_individual(limit=limit, offset=offset),
        "limit": limit,
        "offset": offset,
    }



@app.get(
    "/analytics/summary",
    tags=["analytics"],
    summary="Osnovna statistika nad integrated_individual",
    description="Vraća osnovne agregate (COUNT, AVG...) iz integrated_individual tablice.",
)
def summary():
    return queries.fetch_summary()


@app.get(
    "/analytics/dt_vs_internet",
    tags=["analytics"],
    summary="DT vs WorldBank (join po godini)",
    description="Spaja dt_yearly i wb_internet_year po Year i vraća serije za vizualizaciju.",
)
def dt_vs_internet():
    return {"rows": queries.fetch_dt_vs_internet()}
