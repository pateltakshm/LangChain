"""Module 6 solution — one question, two different tools.

The model reads two different needs in one sentence and picks the right
tool for each — purely from your docstrings. Good tool descriptions are
the real skill here.
"""

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
    rates = {"USD": 1.09, "GBP": 0.85, "JPY": 168.2}
    return rates.get(currency.upper(), 1.0)


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    fake = {"paris": "sunny, 24°C", "london": "rainy, 16°C", "tokyo": "cloudy, 22°C"}
    return fake.get(city.lower(), "no data for this city")


tools = {"multiply": multiply,
         "get_exchange_rate": get_exchange_rate,
         "get_weather": get_weather}
llm_with_tools = ChatOpenAI(model="gpt-4o-mini").bind_tools(list(tools.values()))

question = "What's the weather in Paris, and what is 250 euros in pounds?"
ai_msg = llm_with_tools.invoke(question)
print(ai_msg.tool_calls)   # two work orders: get_weather + get_exchange_rate

messages = [("human", question), ai_msg]
for call in ai_msg.tool_calls:
    messages.append(tools[call["name"]].invoke(call))

print(llm_with_tools.invoke(messages).content)
