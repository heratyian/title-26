from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

COLLECTION_NAME = "title_26"
EMBEDDING_MODEL = "text-embedding-3-small"


def build_vector_store(
    documents: list[Document],
    persist_directory: str = "chroma",
) -> Chroma:
    """Embed documents and save them in a persistent Chroma collection."""
    return Chroma.from_documents(
        documents=documents,
        embedding=OpenAIEmbeddings(model=EMBEDDING_MODEL),
        persist_directory=persist_directory,
        collection_name=COLLECTION_NAME,
    )


def load_vector_store(
    persist_directory: str = "chroma",
) -> Chroma:
    """Open the existing persistent Chroma collection."""
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=OpenAIEmbeddings(model=EMBEDDING_MODEL),
        persist_directory=persist_directory,
    )
