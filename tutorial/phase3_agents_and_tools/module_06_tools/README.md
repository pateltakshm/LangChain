# Module 6 — Tools and Function Calling

## The idea

LLMs are bad at arithmetic and cannot see today's data. **Tools** fix this. A tool is a
normal Python function with a good description. You show the model your toolbox with
`bind_tools()`. The model never runs code — instead, when it decides a tool is needed, it
replies with a structured request: *"call `multiply` with a=12.5, b=8"*. Your code runs the
function and sends the result back.

> **Mental model:** the LLM is a *manager who cannot leave the office*. You give them a phone
> directory (the tool descriptions). When a task needs outside work, the manager doesn't do
> it — they *fill out a work order*: who to call and with what arguments. You (the code) make
> the call and report the result back, and the manager writes the final answer.

## Real-world use case

A finance chatbot asked "What's 17.5% of our 84,300 € budget?" must not guess the math. It
calls a calculator tool, gets the exact number, and phrases the answer nicely — LLM for
language, tools for facts.

## Run it

```bash
python tutorial/phase3_agents_and_tools/module_06_tools/module_6.py
```

Three keys in the code:
- The `@tool` decorator turns a function into a tool — and the **docstring is the tool's job
  advertisement**; it's how the model decides when to use it.
- The type hints (`a: float`) tell the model what arguments to send.
- Notice the loop: model requests → you execute → model concludes. In Module 7, an agent
  runs this loop for you automatically.

**Real search tools:** for live web search, install a search tool such as Tavily
(`pip install langchain-tavily`, free API key at tavily.com) and add
`TavilySearch(max_results=3)` to your tool list — the pattern stays exactly the same.

## 🏆 Challenge 6 — Add a weather tool

Write a `get_weather(city: str)` tool that returns fake data (a small dictionary of cities →
"sunny, 24°C"). Then ask: *"What's the weather in Paris, and what is 250 euros in pounds?"* —
a question that needs **two different tools**. Print `ai_msg.tool_calls` and verify the model
requested both.

<details><summary><b>Hint</b></summary>

Just add a third `@tool` function to the `tools` dictionary. The execution loop already
handles any number of tool calls — that's why it's a loop.
</details>

Solution: [`solution_6.py`](solution_6.py)
