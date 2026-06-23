from app.core.ai_models import AIModels

from langchain_huggingface import HuggingFaceEmbeddings

def _get_embeddings() -> HuggingFaceEmbeddings:
    if AIModels.embeddings is None:
        raise RuntimeError(
            "Embedding 模型尚未加载，请先调用 AIModels.load_models()"
        )
    return AIModels.embeddings

def embed_documents(texts: list[str]) -> list[list[float]]:
    valid_texts = [
        text.strip()
        for text in texts
        if text.strip()
    ]

    if not valid_texts:
        raise ValueError(
            "没有可用于向量化的文本"
        )

    embeddings = _get_embeddings()
    return embeddings.embed_documents(valid_texts)

def embed_query(text: str) -> list[float]:
    text = text.strip()
    if not text:
        raise ValueError(
            "query不能为空"
        )

    embeddings = _get_embeddings()
    return embeddings.embed_query(text)