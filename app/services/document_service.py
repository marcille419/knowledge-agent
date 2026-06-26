import os
import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk
from app.models.document import Document
from app.services.chunk_service import split_text
from app.services.document_parser import parse_document
from app.services.embedding_service import embed_documents
from app.core.vector_store import VectorStore

logger = logging.getLogger(__name__)

def save_chunks(
    document_id : int,
    chunks : list[dict],
    db : Session
):
    if not chunks:
        return []

    chunk_objects = [
        DocumentChunk(
            document_id = document_id,
            chunk_index = chunk["chunk_index"],
            content = chunk["content"]
        )
        for chunk in chunks
    ]

    db.add_all(chunk_objects)
    db.flush()
    return chunk_objects

def process_document(
    document: Document,
    db : Session
):
    if not os.path.exists(document.file_path):
        raise HTTPException(
            status_code=404,
            detail="文件不存在"
        )
    try:
        # 删除该文档的所有旧chunk和向量（同步数据库）
        db.query(DocumentChunk).filter(
            DocumentChunk.document_id == document.id
        ).delete(
            synchronize_session = False
        )

        VectorStore.delete_document(document.id)

        # 解析文件内容
        content = parse_document(document.file_path)

        # 切分文本
        chunks = split_text(content)
        chunks = [
            c
            for c in chunks
            if c.get("content", "").strip()
        ]
        if not chunks:
            raise ValueError(
                f"文档 {document.id} 没有有效文本块"
            )

        # 保存 chunk 并获取回填主键的对象
        chunk_objects = save_chunks(document.id, chunks, db)

        # 生成向量
        texts = [
            chunk.content
            for chunk in chunk_objects
        ]
        embeddings = embed_documents(texts)

        # 构造向量ID和metadata
        ids = [
            f"doc_{document.id}_chunk_{chunk.chunk_index}"
            for chunk in chunk_objects
        ]
        metadatas = [
            {
                "document_id": document.id,
                "chunk_id": chunk.id,
                "user_id": document.user_id,
            }
            for chunk in chunk_objects
        ]

        # 写入向量数据库
        VectorStore.add_embeddings(
            ids=ids,
            embeddings = embeddings,
            metadatas = metadatas,
        )

        # 提交数据库
        db.commit()

        logger.info(
            "文档 %d 处理完成，共 %d 个 chunk 已入库并向量化",
            document.id,
            len(chunk_objects)
        )

    except Exception:
        db.rollback()
        logger.exception("文档 %d 处理失败", document.id)
        raise

# 后期重构内容: Service层最好不要依赖HTTPException