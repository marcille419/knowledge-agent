from typing import Optional
import logging

from langchain_huggingface import HuggingFaceEmbeddings

from app.core.config import settings

logger = logging.getLogger(__name__)

class AIModels:
    embeddings: Optional[HuggingFaceEmbeddings] = None
    llm = None #接入deepseek后再补类型

    @classmethod
    def load_models(cls):
        try:
            logger.info(
                f"开始加载Embedding模型: {settings.EMBEDDING_MODEL}"
            )

            cls.embeddings = HuggingFaceEmbeddings(
                model_name=settings.EMBEDDING_MODEL,
                model_kwargs={"device": "cpu"},
            )

            logger.info("Embedding模型加载成功")

        except Exception:
            logger.exception("Embedding模型加载失败")
            raise