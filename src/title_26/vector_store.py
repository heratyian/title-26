# vectorstore.py

from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings


def build_vector_store(
    chunks,
    persist_directory: str = "chroma",
):
    documents = [
        Document(
            page_content=chunk.text,
            metadata={
                "citation": chunk.citation,
                "section": chunk.section,
                "section_title": chunk.section_title,
                "subsection": chunk.subsection,
                "chapter": chunk.chapter,
                "subchapter": chunk.subchapter,
            },
        )
        for chunk in chunks
    ]

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    return Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name="title_26",
    )

def load_vector_store(
    persist_directory: str = "chroma",
):
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    return Chroma(
        collection_name="title_26",
        embedding_function=embeddings,
        persist_directory=persist_directory,
    )