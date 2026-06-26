import logging
from chromadb import PersistentClient
from chromadb.api.models.Collection import Collection
from typing import Optional, Any, TypedDict

from app.core.config import settings

logger = logging.getLogger(__name__)

class VectorSearchResult(TypedDict):
    chunk_id: int
    document_id: int
    distance: float

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
        if len(ids) != len(embeddings):
            raise ValueError(
                "ids 与 embeddings 数量不一致"
            )

        if metadatas is not None and len(ids) != len(metadatas):
            raise ValueError(
                "ids 与 metadatas 数量不一致"
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
    ) -> None:
        collection = cls._ensure_collection()

        try:
            collection.delete(
                where={
                    "document_id": document_id
                }
            )

            logger.info(
                "成功删除文档 %s 的向量数据",
                document_id
            )

        except Exception:
            logger.exception(
                "删除文档 %s 向量失败",
                document_id
            )
            raise

    @classmethod
    def search(
            cls,
            query_embedding: list[float],
            top_k: int = 5,
            where: Optional[dict[str, Any]] = None
    ) -> list[VectorSearchResult]:
        collection = cls._ensure_collection()

        if not query_embedding:
            raise ValueError("query_embedding不能为空")
        if top_k <= 0:
            raise ValueError("top_k 必须大于 0")

        try:
            results = collection.query(
                query_embeddings = [query_embedding],
                n_results = top_k,
                where = where
            )

            metadatas = results.get("metadatas", [[]])[0]
            distances = results.get("distances", [[]])[0]

            search_results: list[VectorSearchResult] = []

            for metadata, distance in zip(metadatas, distances):
                if metadata is None:
                    continue

                search_results.append(
                    {
                        "chunk_id": int(metadata["chunk_id"]),
                        "document_id": int(metadata["document_id"]),
                        "distance": float(distance),
                    }
                )

            logger.info(
                "向量检索成功，返回 %d 条结果",
                len(search_results)
            )

            return search_results

        except Exception:
            logger.exception(
                "向量检索失败"
            )
            raise
