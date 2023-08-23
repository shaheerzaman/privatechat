from fastapi import FastAPI
import uvicorn

from app import models
from app.db import create_tables
from app.routes import router

app = FastAPI()


@app.on_event("startup")
async def startup():
    create_tables()


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=8000, debug=True)
