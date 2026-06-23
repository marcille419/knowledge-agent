from langchain_huggingface import HuggingFaceEmbeddings

class AIModels:
    embeddings: Optional[HuggingFaceEmbeddings] = None
    llm: Optional[ChatOpenAI] = None

    @classmethod
    def load_models(cls):
        pass