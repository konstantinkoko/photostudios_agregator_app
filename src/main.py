import sys
from fastapi import FastAPI

from agregator.router import router


app = FastAPI(
    title="Agregator App"
)

app.include_router(
    router,
    prefix="/api",
    tags=["API"]
    )
