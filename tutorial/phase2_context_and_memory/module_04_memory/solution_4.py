"""Module 4 solution — proving session isolation.

Session isolation is not optional in real apps — it is both a correctness
and a privacy requirement.
"""

from dotenv import load_dotenv
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful hotel booking assistant."),
    MessagesPlaceholder("history"),
    ("human", "{question}"),
])
chain = prompt | ChatOpenAI(model="gpt-4o-mini") | StrOutputParser()

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

maria = {"configurable": {"session_id": "guest-42"}}
other = {"configurable": {"session_id": "guest-99"}}

print(chatbot.invoke({"question": "Hello, my name is Maria."}, maria))

# Different notebook -> the bot has no idea
print(chatbot.invoke({"question": "What is my name?"}, other))

# Original notebook -> the bot remembers Maria
print(chatbot.invoke({"question": "What is my name?"}, maria))
