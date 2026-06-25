import logging
from typing import Optional, Any
from chromadb import PersistentClient
from chromadb.api.models.Collection import Collection

from app.core.config import settings

logger = logging.getLogger(__name__)

class VectorStore:
    client: Optional[PersistentClient] = None
    collection: Optional[Collection] = None

    @classmethod
    def initialize(cls):
        try:
            logger.info(
                "开始初始化ChromaDB: %s",
                settings.CHROMA_PERSIST_DIR
            )

            cls.client = PersistentClient(path=settings.CHROMA_PERSIST_DIR)
            cls.collection = cls.client.get_or_create_collection(
                name=settings.CHROMA_COLLECTION_NAME
            )

            logger.info(
                "ChromaDB 初始化成功，Collection: %s",
                settings.CHROMA_COLLECTION_NAME,
            )
        except Exception:
            logger.exception("ChromaDB初始化失败")
            raise

    @classmethod
    def _ensure_collection(cls) -> Collection:
        if cls.collection is None:
            raise RuntimeError(
                "VectorStore 尚未初始化，请先调用 initialize()"
            )

        return cls.collection

    @classmethod
    def add_embeddings(
            cls,
            ids: list[str],
            embeddings: list[list[float]],
            metadatas: Optional[list[dict[str, Any]]] = None,
    ) -> None:
        collection = cls._ensure_collection()

        if not ids:
            raise ValueError(
                "ids不能为空"
            )
        if metadatas is not None and len(ids) != len(metadatas):
            raise ValueError(
                "ids 与 embeddings 数量不一致"
            )

        try:
            collection.add(
                ids=ids,
                embeddings=embeddings,
                metadatas=metadatas,
            )

            logger.info(
                "成功写入 %s 条向量",
                len(ids)
            )

        except Exception:
            logger.exception(
                "向量写入失败"
            )

            raise

    @classmethod
    def delete_document(
            cls,
            document_id: int
    ):
        pass
