import argparse

from title_26.rag import Title26RAG


def main() -> None:
    """Run the Title 26 command-line interface."""
    parser = argparse.ArgumentParser(
        description="Ask questions about Title 26."
    )

    parser.add_argument(
        "question",
        help="Question about the U.S. tax code",
    )

    args = parser.parse_args()

    rag = Title26RAG()
    result = rag.ask(args.question)

    print(f"\n{result['answer']}\n\nSources:")

    for source in result["sources"]:
        heading = f" — {source['heading']}" if source.get("heading") else ""
        print(f"- {source['citation']}{heading}")


if __name__ == "__main__":
    main()
