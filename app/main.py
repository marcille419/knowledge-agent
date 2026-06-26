from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routers.user import router as user_routers
from app.routers.document import router as document_router
from app.routers.chat import router as chat_router
from app.core.ai_models import AIModels
from app.core.vector_store import VectorStore


@asynccontextmanager
async def lifespan(app: FastAPI):
    AIModels.load_models()
    VectorStore.initialize()

    yield

    # 后续预留
    # Chroma关闭
    # Redis关闭
    # 模型释放


app = FastAPI(
    title="Knowledge Agent",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(user_routers)
app.include_router(document_router)
app.include_router(chat_router)


@app.get("/")
def home():
    return {
        "message": "Knowledge Agent Running"
    }