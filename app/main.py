from fastapi import FastAPI

app = FastAPI(
    title="Notification Platform",
)


@app.get("/")
def root():
    return {
        "message": "Notification Platform is running"
    }