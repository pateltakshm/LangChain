"""Module 6 — Function calling: the model requests, your code executes."""

from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

load_dotenv()


@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers and return the exact result."""
    return a * b


@tool
def get_exchange_rate(currency: str) -> float:
    """Get today's exchange rate from EUR to the given currency code (e.g. 'USD')."""
    rates = {"USD": 1.09, "GBP": 0.85, "JPY": 168.2}   # fake data for the demo
    return rates.get(currency.upper(), 1.0)


tools = {"multiply": multiply, "get_exchange_rate": get_exchange_rate}
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(list(tools.values()))

question = "How many US dollars is 250 euros?"
ai_msg = llm_with_tools.invoke(question)

# The model did NOT answer — it filled out work orders:
print(ai_msg.tool_calls)
# [{'name': 'get_exchange_rate', 'args': {'currency': 'USD'}, 'id': '...'}]

# Execute each requested tool and collect the results
messages = [("human", question), ai_msg]
for call in ai_msg.tool_calls:
    result = tools[call["name"]].invoke(call)   # runs the real function
    messages.append(result)                     # a ToolMessage with the output

# Send the results back so the model can write the final answer
final = llm_with_tools.invoke(messages)
print(final.content)
