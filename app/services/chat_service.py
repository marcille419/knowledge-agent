from sqlalchemy.orm import Session
from textwrap import dedent

from app.models.document_chunk import DocumentChunk
from app.services.llm_service import generate_answer
from app.services.retrieval_service import retrieve_relevant_chunks

def build_content_preview(content: str, max_length: int = 120) -> str:
    content = content.strip().replace("\n", " ")

    if len(content) <= max_length:
        return content

    return content[:max_length] + "..."


def build_sources(chunks: list[DocumentChunk]) -> list[dict]:
    sources = []

    for index, chunk in enumerate(chunks, start=1):
        filename = None

        if chunk.document is not None:
            filename = chunk.document.filename

        sources.append(
            {
                "source_index": index,
                "chunk_id": chunk.id,
                "document_id": chunk.document_id,
                "filename": filename,
                "chunk_index": chunk.chunk_index,
                "content_preview": build_content_preview(chunk.content),
            }
        )

    return sources

def build_context(chunks: list[DocumentChunk]) -> str:
    if not chunks:
        return ""

    context_parts = []

    for index, chunk in enumerate(chunks, start=1):
        context_parts.append(
            f"[资料{index}]\n{chunk.content}"
        )

    return "\n\n".join(context_parts)

def build_prompt(query: str, context: str) -> str:
    template = dedent("""
        你是一个知识库问答助手。

        请严格根据下面的资料回答用户问题，关键事实尽量使用资料原文表述。
        如果资料中没有答案，请回答：根据已提供资料无法回答该问题。
        不要编造资料之外的内容。

        资料：
        {context}

        用户问题：
        {query}

        回答：
        """).strip()

    return template.format(
        context=context,
        query=query
    )

def answer_question(
        query: str,
        user_id: int,
        db: Session,
        top_k: int = 5,
        debug: bool = False
) -> dict:
    chunks = retrieve_relevant_chunks(
        query=query,
        user_id=user_id,
        db=db,
        top_k=top_k
    )

    context = build_context(chunks)
    prompt = build_prompt(query, context)
    answer = generate_answer(prompt)

    result = {
        "query": query,
        "answer": answer,
        "sources": build_sources(chunks)
    }

    if debug:
        result["prompt"] = prompt

    return result