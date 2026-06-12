from fastapi import FastAPI

from app.routers.user import router as user_routers
from app.routers.document import router as document_router

app = FastAPI(
    title = "Knowledge Agent",
    version = "1.0.0",
)

app.include_router(user_routers)
app.include_router(document_router)

@app.get("/")
def home():
    return {
        "message" : "Knowledge Agent Running"
    }

