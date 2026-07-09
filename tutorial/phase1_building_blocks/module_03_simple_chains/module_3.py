"""Module 3 — The LCEL assembly line: invoke, batch, and stream."""

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a witty marketing copywriter."),
    ("human", "Write one short tagline for a {product} aimed at {audience}."),
])
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.9)
parser = StrOutputParser()  # unwraps the message so you get a plain string

# The assembly line: input -> prompt -> model -> string
chain = prompt | llm | parser

# 1. Run one input
print(chain.invoke({"product": "smart water bottle", "audience": "hikers"}))

# 2. Run many inputs in parallel
results = chain.batch([
    {"product": "noise-canceling headphones", "audience": "students"},
    {"product": "standing desk", "audience": "gamers"},
])
print(results)

# 3. Stream the answer word by word
for piece in chain.stream({"product": "electric bike", "audience": "commuters"}):
    print(piece, end="", flush=True)
print()
