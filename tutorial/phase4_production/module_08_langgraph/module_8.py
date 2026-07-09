"""Module 8 — A writer/critic loop with LangGraph."""

from typing import TypedDict

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini")


# 1. The clipboard: what travels through the graph
class State(TypedDict):
    topic: str
    draft: str
    feedback: str
    attempts: int


# 2. The stations: plain functions that read state and return updates
def writer(state: State) -> dict:
    note = f"\nA reviewer said: {state['feedback']}. Fix that." if state["feedback"] else ""
    draft = llm.invoke(
        f"Write a 3-sentence marketing email about {state['topic']}.{note}"
    ).content
    return {"draft": draft, "attempts": state["attempts"] + 1}


def critic(state: State) -> dict:
    verdict = llm.invoke(
        "You are a strict editor. If this email is clear, specific and under 60 words, "
        "reply exactly APPROVED. Otherwise give one short improvement instruction.\n\n"
        + state["draft"]
    ).content
    return {"feedback": verdict}


# 3. The junction: decide where to go next
def should_continue(state: State) -> str:
    if "APPROVED" in state["feedback"] or state["attempts"] >= 3:
        return "finish"
    return "revise"


# 4. Draw the floor plan
graph = StateGraph(State)
graph.add_node("writer", writer)
graph.add_node("critic", critic)
graph.add_edge(START, "writer")
graph.add_edge("writer", "critic")
graph.add_conditional_edges("critic", should_continue,
                            {"revise": "writer", "finish": END})  # the cycle!

app = graph.compile()
result = app.invoke({"topic": "a reusable coffee cup", "draft": "",
                     "feedback": "", "attempts": 0})

print(f"Approved after {result['attempts']} attempt(s):\n\n{result['draft']}")
