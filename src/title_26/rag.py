# rag.py

from langchain_openai import ChatOpenAI

from title_26.prompts import PROMPT
from title_26.retrieval import create_retriever
from title_26.vector_store import load_vector_store

class Title26RAG:
    def __init__(self):
        vector_store = load_vector_store()

        self.retriever = create_retriever(vector_store)

        self.llm = ChatOpenAI(
            model="gpt-4.1-mini",
            temperature=0,
        )

    def ask(self, question: str) -> dict:
        docs = self.retriever.invoke(question)

        context = "\n\n".join(
            f"{doc.metadata['citation']} — "
            f"{doc.metadata.get('heading', '')}\n"
            f"{doc.page_content}"
            for doc in docs
        )

        chain = PROMPT | self.llm

        response = chain.invoke({
            "context": context,
            "question": question,
        })

        return {
            "answer": response.content,
            "sources": [
                {
                    "citation": doc.metadata["citation"],
                    "heading": doc.metadata.get("heading"),
                }
                for doc in docs
            ],
        }