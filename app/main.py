from fastapi import FastAPI
from app.accounts.routes import router as accounts_router

app = FastAPI(
    title="Client Analytics Async",
    description="Analytics API Platform built with FastAPI",
    version="1.0.0",
)

app.include_router(accounts_router)