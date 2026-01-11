API folder

Contains a lightweight FastAPI skeleton:

- `main.py` exposes `/api/prices/{ticker}` and `/api/health`.

Run with:

```powershell
uvicorn api.main:app --reload --port 8001
```
