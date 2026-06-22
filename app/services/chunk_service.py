from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_text(content: str) -> list[dict]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 50
    )

    chunks = text_splitter.split_text(content)

    return [
        {
            "chunk_index" : i,
            "content" : chunk,
        }
        for i, chunk in enumerate(chunks)
    ]
