import json
from pathlib import Path

from langchain_core.documents import Document
from dotenv import load_dotenv

from title_26.vector_store import build_vector_store


INPUT_PATH = Path("data/processed/usc26.jsonl")


def load_documents(path: Path) -> list[Document]:
    """Load normalized JSONL records as LangChain documents."""
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


def main() -> None:
    """Build the persistent vector index from the normalized dataset."""
    load_dotenv()
    documents = load_documents(INPUT_PATH)
    build_vector_store(documents)

    print(f"Indexed {len(documents)} documents")


if __name__ == "__main__":
    main()
