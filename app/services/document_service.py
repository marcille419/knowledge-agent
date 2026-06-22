import os

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk
from app.models.document import Document
from app.services.chunk_service import split_text
from app.services.document_parser import parse_document


def save_chunks(
    document_id : int,
    chunks : list[dict],
    db : Session
):
    if not chunks:
        return

    chunk_objects = [
        DocumentChunk(
            document_id = document_id,
            chunk_index = chunk["chunk_index"],
            content = chunk["content"]
        )
        for chunk in chunks
    ]

    db.bulk_save_objects(chunk_objects)

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
        db.query(DocumentChunk).filter(
            DocumentChunk.document_id == document.id
        ).delete(
            synchronize_session = False
        )

        content = parse_document(document.file_path)

        chunks = split_text(content)

        save_chunks(document.id, chunks, db)
        db.commit()

    except Exception:
        db.rollback()
        raise

# 后期重构内容: Service层最好不要依赖HTTPException