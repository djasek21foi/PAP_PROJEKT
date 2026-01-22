from __future__ import annotations

from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

from src.db import queries  

app = Flask(__name__)

def get_int_param(name: str, default: int, min_v: int | None = None, max_v: int | None = None) -> int:
    raw = request.args.get(name, None)
    if raw is None:
        value = default
    else:
        try:
            value = int(raw)
        except ValueError:
            raise ValueError(f"Parametar '{name}' mora biti cijeli broj.")
    if min_v is not None and value < min_v:
        raise ValueError(f"Parametar '{name}' mora biti >= {min_v}.")
    if max_v is not None and value > max_v:
        raise ValueError(f"Parametar '{name}' mora biti <= {max_v}.")
    return value


@app.errorhandler(ValueError)
def handle_value_error(e):
    # npr. krivi limit/offset ili nepoznata tablica
    return jsonify({"detail": str(e)}), 400


@app.errorhandler(HTTPException)
def handle_http_exception(e: HTTPException):
    return jsonify({"detail": e.description}), e.code


@app.get("/")
def root():
    return jsonify({
        "status": "ok",
        "how_to_test": [
            "GET /tables",
            "GET /integrated_individual?limit=5",
            "GET /analytics/summary",
            "GET /analytics/dt_vs_internet",
        ],
        "examples": {
            "tables": "/tables",
            "any_table_example": "/table/integrated_individual?limit=5&offset=0",
        },
    })


@app.get("/tables")
def tables():
    return jsonify({"tables": queries.list_tables()})


@app.get("/table/<table_name>")
def any_table(table_name: str):
    limit = get_int_param("limit", default=100, min_v=1, max_v=1000)
    offset = get_int_param("offset", default=0, min_v=0)

    rows = queries.fetch_all(table_name, limit=limit, offset=offset)
    return jsonify({"table": table_name, "rows": rows, "limit": limit, "offset": offset})


@app.get("/dt_yearly")
def dt_yearly():
    limit = get_int_param("limit", default=100, min_v=1, max_v=1000)
    offset = get_int_param("offset", default=0, min_v=0)
    return jsonify({"rows": queries.fetch_dt_yearly(limit=limit, offset=offset),
                    "limit": limit, "offset": offset})


@app.get("/wb_internet_year")
def wb_internet_year():
    limit = get_int_param("limit", default=100, min_v=1, max_v=1000)
    offset = get_int_param("offset", default=0, min_v=0)
    return jsonify({"rows": queries.fetch_wb_internet_year(limit=limit, offset=offset),
                    "limit": limit, "offset": offset})


@app.get("/integrated_individual")
def integrated_individual():
    limit = get_int_param("limit", default=100, min_v=1, max_v=1000)
    offset = get_int_param("offset", default=0, min_v=0)
    return jsonify({"rows": queries.fetch_integrated_individual(limit=limit, offset=offset),
                    "limit": limit, "offset": offset})


@app.get("/analytics/summary")
def summary():
    return jsonify(queries.fetch_summary())


@app.get("/analytics/dt_vs_internet")
def dt_vs_internet():
    return jsonify({"rows": queries.fetch_dt_vs_internet()})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
