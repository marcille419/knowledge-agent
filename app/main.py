from fastapi import FastAPI
from app.routers.user import router as user_routers

app = FastAPI(
    title = "Knowledge Agent",
    version = "1.0.0",
)

app.include_router(user_routers)

@app.get("/")
def home():
    return {
        "message" : "Knowledge Agent Running"
    }

