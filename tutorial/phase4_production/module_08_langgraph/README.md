# Module 8 — LangGraph: Cyclical Workflows and State Machines

## The idea

Chains flow in one direction: A → B → C, done. But real workflows need **loops** ("keep
improving until it's good") and **branches** ("if the answer is weak, try again; otherwise
finish"). **LangGraph** models your app as a graph: **nodes** are steps (functions),
**edges** are the paths between them, and a shared **state** object travels through the
graph, collecting results.

> **Mental model:** a chain is an assembly line; LangGraph is the *whole factory floor plan*.
> The state is a *clipboard attached to the product*: every station reads it, does its work,
> and writes an update. Crucially, the floor plan can include a *quality-control station that
> sends the product back* for rework — a cycle, which plain chains cannot do.

## Real-world use case

An email-writing service where a "writer" drafts, a "critic" reviews, and drafts loop back
until the critic approves (or a retry limit is hit). This draft–review–revise cycle is the
backbone of most production agent systems.

## Run it

```bash
python tutorial/phase4_production/module_08_langgraph/module_8.py
```

The magic line is `add_conditional_edges`: after the critic runs, `should_continue` inspects
the state and routes either back to the writer (a cycle) or to `END`. The `attempts >= 3`
guard matters — **every cycle in production needs an exit condition**, or one stubborn critic
burns your API budget forever.

## 🏆 Challenge 8 — Add a third station

After approval, add a `translator` node that translates the final draft into French and
stores it in a new state field `translation`. Route: critic approves → translator → END
(rework still loops to the writer). Print both versions at the end.

<details><summary><b>Hint</b></summary>

- Add `translation: str` to `State`.
- Write a `translator(state)` function that returns `{"translation": ...}`.
- Register it with `add_node`.
- Change the conditional mapping to `{"revise": "writer", "finish": "translator"}`.
- Add `graph.add_edge("translator", END)`.
</details>

Solution: [`solution_8.py`](solution_8.py)
