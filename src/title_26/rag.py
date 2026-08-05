from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from title_26.vector_store import load_vector_store


PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an educational assistant for exploring Title 26 of the United States Code.
        Answer questions using only the supplied context. If the context is insufficient, say so.
        Cite relevant sections using their U.S.C. citation. Do not present the response as professional tax advice.
        """,
    ),
    ("human", "Context:\n\n{context}\n\nQuestion:\n\n{question}"),
])


class Title26RAG:
    """Answer questions using sections retrieved from the Title 26 index."""

    def __init__(self) -> None:
        load_dotenv()
        self.retriever = load_vector_store().as_retriever(
            search_kwargs={"k": 5},
        )
        self.chain = PROMPT | ChatOpenAI(model="gpt-4.1-mini", temperature=0)

    def ask(self, question: str) -> dict:
        """Return a grounded answer and the retrieved source citations."""
        docs = self.retriever.invoke(question)

        context = "\n\n".join(
            f"{doc.metadata['citation']} — "
            f"{doc.metadata.get('heading', '')}\n"
            f"{doc.page_content}"
            for doc in docs
        )

        response = self.chain.invoke({
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
