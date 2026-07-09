"""Module 7 — A ReAct agent that plans its own tool use."""

from dotenv import load_dotenv
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

load_dotenv()


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    fake = {"tokyo": "cloudy, 22°C", "osaka": "sunny, 26°C", "yokohama": "rainy, 20°C"}
    return fake.get(city.lower(), "no data for this city")


@tool
def calculator(expression: str) -> str:
    """Evaluate a math expression like '250 * 0.85'. Use for ALL arithmetic."""
    return str(eval(expression, {"__builtins__": {}}))  # demo only — never in production


agent = create_react_agent(
    model="openai:gpt-4o-mini",
    tools=[get_weather, calculator],
    prompt="You are a precise assistant. Use tools instead of guessing.",
)

result = agent.invoke({
    "messages": [("human",
        "What's the weather in Tokyo and Osaka? Also, what is 15% of 3400?")]
})

# Watch the agent think, act, and observe:
for msg in result["messages"]:
    msg.pretty_print()
