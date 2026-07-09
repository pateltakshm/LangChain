"""Module 3 solution — a two-step chain (name -> slogan).

Chaining chains is how you break big tasks into small, reliable steps —
each step gets a focused prompt instead of one giant confusing one.
"""

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.9)
parser = StrOutputParser()

name_prompt = ChatPromptTemplate.from_template(
    "Invent a catchy company name for a business in the {industry} industry. "
    "Reply with only the name."
)
slogan_prompt = ChatPromptTemplate.from_template(
    "Write a one-sentence slogan for a company called {name}."
)

name_chain = name_prompt | llm | parser

# The output of name_chain becomes the {name} variable of slogan_prompt
full_chain = {"name": name_chain} | slogan_prompt | llm | parser

print(full_chain.invoke({"industry": "organic coffee"}))
