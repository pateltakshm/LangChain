# Module 9 — Evaluation and Monitoring with LangSmith

## The idea

LLM apps fail silently: no exception, just a wrong or mediocre answer. So production work
needs two practices normal software doesn't emphasize as much:

- **Tracing:** recording every step of every run — which prompt was sent, what the retriever
  returned, how long each step took, what it cost.
- **Evaluation:** keeping a test set of questions with known good answers, and scoring your
  app against it every time you change a prompt or model.

> **Mental model:** LangSmith is the *flight recorder plus the flight simulator*. The flight
> recorder (tracing) captures everything, so after a bad answer you can replay exactly what
> happened at every station of your assembly line. The simulator (evaluation) lets you test a
> new prompt against 50 known scenarios *before* real passengers board.

## Real-world use case

Your RAG bot from Module 5 gives a wrong answer in production. Was the retriever fetching the
wrong chunks, or did the LLM ignore good context? Without tracing you're guessing; with
LangSmith you open the trace, see each step's inputs and outputs, and know in one minute.

## Part 1 — Tracing (zero code changes)

Create a free account at <https://smith.langchain.com>, get an API key, and add three lines
to your `.env` in the repo root:

```
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=lsv2-your-key-here
LANGSMITH_PROJECT=langchain-course
```

That's the whole integration. Re-run *any* earlier module, open the LangSmith website, and
you'll see a full trace: the exact prompt after template filling, retrieved chunks, every
agent tool call, plus latency and token cost per step.

## Part 2 — Evaluation

```bash
python tutorial/phase4_production/module_09_langsmith/module_9.py
```

The script uses **LLM-as-judge**: a second model compares your app's answer to the reference.
Now every change is measurable — swap `gpt-4o-mini` for another model, rerun, and LangSmith
shows both experiments side by side. Prompt changes stop being guesswork.

## 🏆 Challenge 9 — Add a second quality metric

Write a `conciseness` evaluator that passes only if the answer is under 40 words, add it to
the `evaluators` list, and rerun. Then make it fail on purpose (tell the app to "answer in
great detail") and watch the score drop in the dashboard.

<details><summary><b>Hint</b></summary>

No LLM needed for this one — evaluators are just functions: count
`len(outputs["answer"].split())` and return a boolean. Cheap rule-based checks beside LLM
judges is the standard pattern.
</details>

Solution: [`solution_9.py`](solution_9.py)
