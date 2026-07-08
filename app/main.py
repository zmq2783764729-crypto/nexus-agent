from fastapi import APIRouter, FastAPI

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "ok"}