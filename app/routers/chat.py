from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.services.chat_service import answer_question
from app.services.retrieval_service import retrieve_relevant_chunks

router = APIRouter(
    prefix = "/chat",
    tags = ["chat"]
)

@router.get("/retrieve")
def retrieve_chunks(
    query: str,
    top_k: int = 5,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chunks = retrieve_relevant_chunks(
        query=query,
        user_id=current_user.id,
        db=db,
        top_k=top_k
    )

    return {
        "query": query,
        "total": len(chunks),
        "chunks": [
            {
                "chunk_id": chunk.id,
                "document_id": chunk.document_id,
                "chunk_index": chunk.chunk_index,
                "content": chunk.content,
            }
            for chunk in chunks
        ]
    }

@router.get("/ask")
def ask_question(
    query: str,
    top_k: int = 5,
    debug: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return answer_question(
        query = query,
        user_id = current_user.id,
        db = db,
        top_k = top_k,
        debug = debug
    )