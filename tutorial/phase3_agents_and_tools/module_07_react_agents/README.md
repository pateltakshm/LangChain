# Module 7 — ReAct Agents

## The idea

In Module 6, *you* wrote the loop that executes tools. An **agent** owns that loop itself.
The pattern is called **ReAct** — Reason + Act:

1. **Think:** "What do I need to answer this?"
2. **Act:** call a tool.
3. **Observe:** read the tool's result.
4. Repeat until it has enough to answer — then answer.

> **Mental model:** a chain is a *train on fixed rails* — same stations, every time. An agent
> is a *taxi driver*: you give the destination, and they choose the route turn by turn based
> on what they see. More flexible, but less predictable — which is why Phase 4 teaches you to
> control and measure them.

## Real-world use case

A travel assistant asked "Find the weather in the three biggest cities in Japan" needs
several steps it must plan itself: figure out the cities, then call the weather tool three
times, then summarize. Nobody hard-coded that sequence — the agent decided it.

## Run it

```bash
pip install langgraph   # agents are built on LangGraph (already in requirements.txt)
python tutorial/phase3_agents_and_tools/module_07_react_agents/module_7.py
```

Read the printed transcript — you will literally see the ReAct loop: an AI message with tool
calls (think + act), tool messages with results (observe), sometimes another round, then the
final answer. All the loop code you wrote in Module 6 is now inside `create_react_agent`.

**Version note:** in LangChain 1.0+ the same thing is also exposed as
`from langchain.agents import create_agent`. Older tutorials use `AgentExecutor` and
`initialize_agent` — those are legacy; prefer the LangGraph-based agent shown here.

## 🏆 Challenge 7 — Build a research-and-math agent

Give the agent two tools: a fake `company_lookup(name)` tool that returns a company's revenue
(invent data for 2–3 companies), and the calculator. Then ask: *"What is the combined revenue
of Acme and Globex, and what would a 12% increase make it?"* Check the transcript: did it look
up both companies before calculating?

<details><summary><b>Hint</b></summary>

The agent needs the lookups *before* it can calculate — that ordering is exactly what ReAct
plans for you. Make `company_lookup` return strings like `"Acme revenue: 5,200,000 USD"`.
</details>

Solution: [`solution_7.py`](solution_7.py)
