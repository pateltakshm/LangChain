"""Module 8 solution — adding a translator station after approval.

You extended a state machine without touching the existing nodes — that
isolation is why teams use LangGraph for complex systems.
"""

from typing import TypedDict

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini")


class State(TypedDict):
    topic: str
    draft: str
    feedback: str
    attempts: int
    translation: str          # new field


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


def translator(state: State) -> dict:
    french = llm.invoke(
        "Translate this email into French, keeping the marketing tone:\n\n"
        + state["draft"]
    ).content
    return {"translation": french}


def should_continue(state: State) -> str:
    if "APPROVED" in state["feedback"] or state["attempts"] >= 3:
        return "finish"
    return "revise"


graph = StateGraph(State)
graph.add_node("writer", writer)
graph.add_node("critic", critic)
graph.add_node("translator", translator)
graph.add_edge(START, "writer")
graph.add_edge("writer", "critic")
graph.add_conditional_edges("critic", should_continue,
                            {"revise": "writer", "finish": "translator"})
graph.add_edge("translator", END)

app = graph.compile()
result = app.invoke({"topic": "a reusable coffee cup", "draft": "",
                     "feedback": "", "attempts": 0, "translation": ""})

print("ENGLISH:\n", result["draft"])
print("\nFRENCH:\n", result["translation"])
