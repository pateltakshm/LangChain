# Module 1 — Introduction to LLMs and LangChain

## The idea

A **Large Language Model (LLM)** is a program trained on huge amounts of text. You give it
text, and it predicts what text should come next. That simple trick is powerful enough to
answer questions, write code, and summarize documents.

> **Mental model:** an LLM is a *very well-read employee with no memory and no hands*. It
> knows a lot, but it forgets everything after each conversation, and it cannot open files,
> browse the web, or use a calculator on its own. **LangChain is the office you build around
> this employee** — it gives them instructions (prompts), a notebook (memory), a filing
> cabinet (vector stores), and tools (function calling).

LangChain's key promise: swap one model for another (OpenAI → Anthropic → local) without
rewriting your app.

## Real-world use case

A customer-support team wants to auto-draft replies to common emails: send the email text to
an LLM, get a polite draft back. The simplest possible LLM app — and exactly what this module
builds.

## Run it

```bash
python tutorial/phase1_building_blocks/module_01_llms_and_langchain/module_1.py
```

Three things to notice in the code:
- `load_dotenv()` loads your secret key safely — never paste keys into code.
- `invoke()` is the universal "run it" method you will use on everything in LangChain.
- The reply is an object; the text lives in `response.content`.

## 🏆 Challenge 1 — Build a "Support Draft" bot

Change the script so it takes a customer complaint (stored in a variable) and asks the model
to write a short, apologetic reply that offers a refund. Then run it with `temperature=0`
and `temperature=1` and compare the outputs across several runs.

<details><summary><b>Hint</b></summary>

Build the prompt with an f-string: `f"Write a polite reply to this complaint: {complaint}"`.
Create two `ChatOpenAI` objects with different temperatures and call `invoke()` on each.
</details>

Solution: [`solution_1.py`](solution_1.py) — try it yourself first!
