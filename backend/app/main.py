"""FastAPI application entrypoint."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.init_db import init_db
from app.routers import auth, menu, orders


@asynccontextmanager
async def lifespan(application: FastAPI):
    init_db()
    yield


def create_app() -> FastAPI:
    application = FastAPI(title="Customer Ordering System", lifespan=lifespan)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(auth.router)
    application.include_router(menu.router)
    application.include_router(orders.router)
    return application


app = create_app()
