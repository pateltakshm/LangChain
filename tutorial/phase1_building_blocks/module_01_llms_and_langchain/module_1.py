"""Module 1 — Your first LLM call with LangChain."""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()  # reads OPENAI_API_KEY from your .env file

# temperature controls creativity: 0 = focused and repeatable, 1 = creative
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

response = llm.invoke(
    "Explain what a Large Language Model is in one short, friendly paragraph."
)

print(response.content)
