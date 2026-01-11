Repository structure (prototype)

- `database/` — DB helpers and migration scripts.
- `data/` — data ingestion and generators (e.g., `generate_mock.py`).
- `api/` — FastAPI skeleton and endpoints.
- `ui/` — Streamlit/Front-end prototypes.
- root files — quick scripts and legacy prototypes.

Next steps:
- Move root modules into `database/`, `data/`, and `api/` packages as we stabilize the layout.
