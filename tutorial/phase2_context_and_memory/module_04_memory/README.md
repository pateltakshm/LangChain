# Module 4 — Chat History and Memory

## The idea

Here is a surprise: **LLMs have no memory at all.** When ChatGPT "remembers" your name, it's
because the app silently re-sends the whole conversation with every new message. To build a
chatbot, you must store past messages and include them in each request.

> **Mental model:** imagine a brilliant consultant with *total amnesia*. Every meeting, you
> hand them a *notebook of everything said so far*; they read it in seconds, give a great
> answer — then forget everything again. Memory in LangChain is the notebook, plus a clerk
> (`RunnableWithMessageHistory`) who writes each exchange into it and hands it over at the
> start of every meeting.

## Real-world use case

A hotel booking assistant must remember that the guest already said "2 adults, arriving
Friday" — asking again would feel broken. It also needs **separate notebooks per guest**
(session IDs), so conversations never leak between users.

## Run it

```bash
python tutorial/phase2_context_and_memory/module_04_memory/module_4.py
```

Key pieces in the code:
- `MessagesPlaceholder("history")` marks where the notebook's pages go inside the prompt.
- `RunnableWithMessageHistory` is the clerk: before each call it fetches the right notebook
  by `session_id`; after each call it writes the new exchange in.
- In production you'd swap `InMemoryChatMessageHistory` for a database-backed version
  (Redis, Postgres) — the rest of the code stays identical.

## 🏆 Challenge 4 — Prove that sessions are isolated

Have "guest-42" say their name is Maria. Then, in a *different* session ("guest-99"), ask
"What is my name?". Finally ask the same question back in "guest-42". Confirm the bot only
knows the name in the right session.

<details><summary><b>Hint</b></summary>

Make two config objects with different `session_id` values and pass the right one to each
`invoke()` call:

```python
maria = {"configurable": {"session_id": "guest-42"}}
other = {"configurable": {"session_id": "guest-99"}}
```
</details>

Solution: [`solution_4.py`](solution_4.py)
