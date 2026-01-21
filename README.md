# Utjecaj online sadržaja na dnevne navike i produktivnost.

Projekt analizira kako vrijeme provedeno na internetu i društvenim mrežama utječe na navike i produktivnost.
Podaci se prikupljaju iz više heterogenih izvora (CSV + JSON API), obrađuju i integriraju, spremaju u bazu (SQLite),
te se izlažu kroz REST API (Flask). Na kraju se provodi osnovna analiza i vizualizacija.

## Izvori podataka

Heterogeni izvori (različit format i struktura):

**CSV (Kaggle):**
- Time the Internet (CSV) - https://www.kaggle.com/datasets/willianoliveiragibin/time-the-internet
- Time Wasters on Social Media (CSV) - https://www.kaggle.com/datasets/muhammadroshaanriaz/time-wasters-on-social-media
- Social Media vs Productivity (CSV) - https://www.kaggle.com/datasets/mahdimashayekhi/social-media-vs-productivity
- Time Spent on Social Media (CSV) - https://www.kaggle.com/datasets/patricklford/time-spent-on-social-media

**JSON API:**
- World Bank API – indikator: *Individuals using the Internet (% of population)* (`IT.NET.USER.ZS`)

> Napomena: World Bank indikator nema vrijednosti za sve godine (posebno rane godine), pa su `null` vrijednosti.

## Struktura projekta
PAP_PROJEKT/
  data_raw/            # originalni CSV + raw JSON dump
  data_processed/      # očišćeni/integirani CSV + SQLite (pap.db)
  notebooks/           # 01..04 (dokumentacija + koraci)
  src/
    api/               # FastAPI (main.py)
    db/                # connection.py, queries.py
    etl/               # (opcionalno) skripte za rebuild baze
  scripts/             # pomoćni testovi (test_db.py)
  README.md
  LICENSE
  .gitignore

- `data_raw/` — sirovi (preuzeti) CSV i raw JSON iz API-a
- `data_processed/` — rezultat obrade: integrirani CSV + `pap.db`
- `notebooks/` — dokumentirani koraci projekta (od izvora do analize)
- `src/` — kod za bazu i API
- `scripts/` — brzi testovi (npr. ispis tablica u bazi)

## Bilježnice (notebooks)

1. **01_data_collection.ipynb**
   - učitavanje CSV datoteka
   - poziv World Bank API-ja i spremanje raw JSON-a u `data_raw/`

2. **02_preprocessing_integration.ipynb**
   - čišćenje (tipovi, nedostajuće vrijednosti)
   - agregacije / priprema tablica za integraciju
   - spremanje rezultata u `data_processed/`

3. **03_database.ipynb**
   - kreiranje SQLite baze `pap.db`
   - zapis tablica u bazu (`to_sql`)
   - provjera SELECT upita

4. **04_analysis.ipynb**
   - osnovna statistika i vizualizacije
   - primjer spajanja (DT minutes vs WorldBank internet % po godinama)
   - korelacija / osnovni uvidi
  
## Pokretanje projekta
Iz root foldera projekta:
python -m uvicorn src.api.main:app --reload

Otvorit će se:
Swagger UI: http://127.0.0.1:8000/docs
OpenAPI JSON: http://127.0.0.1:8000/openapi.json
