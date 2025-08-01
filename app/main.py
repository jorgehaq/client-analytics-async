from fastapi import FastAPI
from app.accounts.routes import router as accounts_router
from app.datasets.routes import router as datasets_router


app = FastAPI(
    title="Client Analytics Async",
    description="Analytics API Platform built with FastAPI",
    version="1.0.0",
)

app.include_router(accounts_router)
app.include_router(datasets_router)