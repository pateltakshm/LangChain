"""Module 2 — Reusable prompts with ChatPromptTemplate."""

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a professional translator. Translate the user's text "
               "into {language}. Keep the tone {tone}. Reply with only the translation."),
    ("human", "{text}"),
])

# Fill in the blanks -> produces a list of ready-to-send messages
messages = prompt.invoke({
    "language": "Spanish",
    "tone": "casual",
    "text": "Hey! The hotel was amazing, you should totally go.",
})

print(llm.invoke(messages).content)
