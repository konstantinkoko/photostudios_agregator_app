from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from agregator.router import router as agregator_api_router
from web_interface.router import router as web_interface_router


app = FastAPI(
    title="Agregator App"
)

app.mount("/static", StaticFiles(directory="../static"), name="static")

app.include_router(
    agregator_api_router,
    prefix="/api",
    tags=["API"]
    )

app.include_router(
    web_interface_router,
    tags=["WEB interface"]
    )

