# cli.py

import argparse

from title_26.rag import Title26RAG
import title_26.config


def main():
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

    print()
    print(result["answer"])

    print("\nSources:")

    for source in result["sources"]:
        print(
            f"- {source['citation']} — "
            f"{source.get('heading')}"
        )


if __name__ == "__main__":
    main()