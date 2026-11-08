from fastapi import FastAPI

app = FastAPI(
    title="Notification Platform",
)


@app.get("/")
def root():
    return {
        "message": "Notification Platform is running"
    }


@app.get("/health", tags=["health"])
def health_check():
    """Lightweight liveness probe for containers and orchestrators."""
    return {"status": "healthy"}
