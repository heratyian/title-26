import json
from pathlib import Path

from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

import title_26.config


INPUT_PATH = Path("data/processed/usc26.jsonl")
CHROMA_PATH = "chroma"


def load_documents(path: Path) -> list[Document]:
    documents = []

    with path.open(encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)

            documents.append(
                Document(
                    page_content=record["text"],
                    metadata={
                        "title": record["title"],
                        "section": record["section"],
                        "heading": record["heading"],
                        "citation": record["citation"],
                    },
                )
            )

    return documents


def main():
    docs = load_documents(INPUT_PATH)

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=CHROMA_PATH,
        collection_name="title_26",
    )

    print(f"Indexed {len(docs)} documents")


if __name__ == "__main__":
    main()