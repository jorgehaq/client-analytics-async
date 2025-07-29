from fastapi import FastAPI


app = FastAPI(
    title="Client Analytics Async",
    description="Analytics API Platform built with FastAPI",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint to verify the service is up and running."""
    return {"status": "ok"}
