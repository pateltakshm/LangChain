"""Module 5 — RAG: load, split, embed, store, retrieve, answer."""

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# --- PHASE A: INDEXING (run once) ---
handbook = Document(page_content="""
Vacation policy: All full-time employees receive 24 paid vacation days per year.
Unused days do not roll over to the next year.
Remote work: Employees may work remotely up to 3 days per week with manager approval.
Equipment: The company provides a laptop and a 300 euro budget for home-office gear.
Sick leave: Sick days are unlimited but require a doctor's note after 3 consecutive days.
""")
# For real files use loaders instead, e.g.:
#   from langchain_community.document_loaders import PyPDFLoader, TextLoader

splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=30)
chunks = splitter.split_documents([handbook])

vector_store = InMemoryVectorStore.from_documents(chunks, OpenAIEmbeddings())
retriever = vector_store.as_retriever(search_kwargs={"k": 2})  # top 2 chunks

# --- PHASE B: THE RAG CHAIN (runs on every question) ---
prompt = ChatPromptTemplate.from_template(
    "Answer the question using ONLY the context below. "
    "If the answer is not in the context, say you don't know.\n\n"
    "Context:\n{context}\n\nQuestion: {question}"
)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | ChatOpenAI(model="gpt-4o-mini", temperature=0)
    | StrOutputParser()
)

print(rag_chain.invoke("How many vacation days do I get, and do they roll over?"))
print(rag_chain.invoke("What is the dress code?"))  # not in the handbook -> "I don't know"
