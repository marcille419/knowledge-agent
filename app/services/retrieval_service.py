import logging

from sqlalchemy.orm import Session, joinedload

from app.models.document_chunk import DocumentChunk
from app.models.document import Document
from app.services.embedding_service import embed_query
from app.core.vector_store import VectorStore

logger = logging.getLogger(__name__)

def retrieve_relevant_chunks(
        query: str,
        user_id: int,
        db: Session,
        top_k: int = 5
) -> list[DocumentChunk]:
    query = query.strip()

    if user_id <= 0:
        raise ValueError("user_id必须大于0")

    if not query:
        raise ValueError("query不能为空")

    if top_k <= 0:
        raise ValueError("top_k必须大于0")

    # 问题向量化
    query_embedding = embed_query(query)

    # 向量检索
    search_results = VectorStore.search(
        query_embedding = query_embedding,
        top_k = top_k,
        where = {
            "user_id": user_id
        }
    )

    if not search_results:
        return []

    # 提取chunk_id
    chunk_ids = [
        result["chunk_id"]
        for result in search_results
    ]

    # mysql回表查询 chunk 内容
    chunks = db.query(DocumentChunk).options(
        joinedload(DocumentChunk.document)
    ).join(Document).filter(
        DocumentChunk.id.in_(chunk_ids),
        Document.user_id == user_id
    ).all()

    # 按向量检索结果的顺序重新排序
    chunk_map = {
        chunk.id: chunk
        for chunk in chunks
    }

    ordered_chunks = [
        chunk_map[result["chunk_id"]]
        for result in search_results
        if result["chunk_id"] in chunk_map
    ]

    logger.info(
        "召回成功，user_id=%s，query=%s，返回 %d 个 chunk",
        user_id,
        query,
        len(ordered_chunks)
    )

    return ordered_chunks