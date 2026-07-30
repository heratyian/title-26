from langchain_core.prompts import ChatPromptTemplate


SYSTEM_PROMPT = """
You are an educational assistant for exploring
Title 26 of the United States Code.

Answer questions using only the supplied context.

If the supplied context does not contain enough information
to answer the question, say so.

Cite relevant sections using their U.S.C. citation.

Do not present the response as professional tax advice.
"""


PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    (
        "human",
        """
        Context:

        {context}

        Question:

        {question}
        """,
    ),
])