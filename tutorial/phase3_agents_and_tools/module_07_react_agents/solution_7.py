"""Module 7 solution — a research-and-math agent.

Expected plan in the transcript: lookup Acme -> lookup Globex -> calculator
with something like (5200000 + 8700000) * 1.12 -> final answer
(~15.57 million USD). If the agent skipped a step, strengthen the prompt —
steering agents with instructions is a core skill.
"""

from dotenv import load_dotenv
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

load_dotenv()


@tool
def company_lookup(name: str) -> str:
    """Look up a company's annual revenue in USD."""
    data = {"acme": 5_200_000, "globex": 8_700_000, "initech": 3_100_000}
    revenue = data.get(name.lower())
    return f"{name} revenue: {revenue} USD" if revenue else "company not found"


@tool
def calculator(expression: str) -> str:
    """Evaluate a math expression like '(5200000 + 8700000) * 1.12'."""
    return str(eval(expression, {"__builtins__": {}}))  # demo only


agent = create_react_agent(
    model="openai:gpt-4o-mini",
    tools=[company_lookup, calculator],
    prompt="You are a financial analyst. Always look up real figures with tools "
           "and use the calculator for every computation. Never guess numbers.",
)

result = agent.invoke({"messages": [("human",
    "What is the combined revenue of Acme and Globex, "
    "and what would a 12% increase make it?")]})

for msg in result["messages"]:
    msg.pretty_print()
