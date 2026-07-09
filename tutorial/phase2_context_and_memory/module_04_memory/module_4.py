"""Module 4 — A chatbot that remembers, with per-session memory."""

from dotenv import load_dotenv
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful hotel booking assistant."),
    MessagesPlaceholder("history"),   # past messages get inserted here
    ("human", "{question}"),
])
chain = prompt | ChatOpenAI(model="gpt-4o-mini") | StrOutputParser()

# One notebook (message history) per session ID
store = {}


def get_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


chatbot = RunnableWithMessageHistory(
    chain,
    get_history,
    input_messages_key="question",
    history_messages_key="history",
)

config = {"configurable": {"session_id": "guest-42"}}

print(chatbot.invoke({"question": "Hi! I need a room for 2 adults on Friday."}, config))
print(chatbot.invoke({"question": "How many adults did I say?"}, config))  # it remembers!
