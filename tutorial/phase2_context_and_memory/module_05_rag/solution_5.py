"""Module 5 solution — RAG with source citations.

Citations turn "trust me" answers into checkable ones — usually the first
feature real users ask for in a RAG app.
"""

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv()

docs = [
    Document(
        page_content="Vacation policy: All full-time employees receive 24 paid "
                     "vacation days per year. Unused days do not roll over.",
        metadata={"source": "handbook-p1"},
    ),
    Document(
        page_content="Remote work: up to 3 days per week with manager approval. "
                     "Equipment: laptop plus a 300 euro home-office budget.",
        metadata={"source": "handbook-p2"},
    ),
]

vector_store = InMemoryVectorStore.from_documents(docs, OpenAIEmbeddings())
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

prompt = ChatPromptTemplate.from_template(
    "Answer using ONLY the context. End your answer with 'Source: <source id>'. "
    "If the answer is not in the context, say you don't know.\n\n"
    "Context:\n{context}\n\nQuestion: {question}"
)


def format_docs(docs):
    return "\n\n".join(
        f"[{doc.metadata['source']}] {doc.page_content}" for doc in docs
    )


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | ChatOpenAI(model="gpt-4o-mini", temperature=0)
    | StrOutputParser()
)

print(rag_chain.invoke("What is the home-office budget?"))
# -> "...300 euros... Source: handbook-p2"
