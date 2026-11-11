from fastapi import FastAPI

app = FastAPI(title="StockPyme")


@app.get("/salud")
def salud():
    return {"estado": "ok"}