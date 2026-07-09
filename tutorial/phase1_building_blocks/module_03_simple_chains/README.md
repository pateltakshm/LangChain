# Module 3 — Simple Chains with LCEL

## The idea

So far you invoked the template, then invoked the model, then read `.content` — three manual
steps. **LCEL (LangChain Expression Language)** lets you glue components together with the
pipe symbol `|`, so the output of one step flows into the next automatically:

```python
chain = prompt | llm | parser
```

> **Mental model:** a chain is an *assembly line*. Raw material (your input dictionary)
> enters at one end. Station 1 (the prompt) shapes it into messages. Station 2 (the model)
> turns messages into an answer. Station 3 (the parser) unwraps the answer into a plain
> string. You just drop material in and collect the finished product.

## Real-world use case

A marketing tool generates product taglines. Chains make this a one-liner to run — and every
chain automatically supports `.batch()` (many inputs at once) and `.stream()` (word-by-word
output, like ChatGPT's typing effect), so you get production features for free.

## Run it

```bash
python tutorial/phase1_building_blocks/module_03_simple_chains/module_3.py
```

That single line — `chain = prompt | llm | parser` — is the heart of modern LangChain. Every
advanced thing you build later (RAG, agents, graphs) is still "components connected so data
flows through them."

## 🏆 Challenge 3 — Build a two-step chain

Step 1: given an `{industry}`, generate a company name (just the name). Step 2: take that
name and write a one-sentence slogan for it. Connect them so **one** `invoke()` call runs
both steps.

<details><summary><b>Hint</b></summary>

Build `name_chain` first. Then start the second chain with a dictionary that maps the
variable name to the first chain:

```python
full_chain = {"name": name_chain} | slogan_prompt | llm | parser
```

LCEL runs the inner chain first and feeds its output into `{name}`.
</details>

Solution: [`solution_3.py`](solution_3.py)
