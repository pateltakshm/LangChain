# Module 5 — Retrieval-Augmented Generation (RAG)

## The idea

An LLM knows nothing about *your* data — your company wiki, your PDFs, yesterday's meeting
notes. **RAG** solves this in two phases:

- **Indexing (done once):** load your documents, split them into small chunks, convert each
  chunk into an **embedding** (a list of numbers that captures its meaning), and store those
  in a **vector store**.
- **Retrieval (every question):** embed the user's question the same way, find the chunks
  whose numbers are most similar, and paste them into the prompt as context.

> **Mental model:** a vector store is a *filing cabinet organized by meaning instead of
> alphabet*. Documents about refunds sit near documents about returns, even if they share no
> words. When a question arrives, a librarian (the retriever) pulls the 3–4 most relevant
> pages and clips them to the question before handing it to the consultant (the LLM), with
> the rule: *"answer only from these pages."*

**Why chunks?** Models have a context limit, and retrieval quality drops when chunks are
huge. Small overlapping chunks (200–1000 characters) mean the librarian can pull exactly the
relevant paragraph, not a whole 80-page manual.

## Real-world use case

An HR chatbot that answers "How many vacation days do I get?" from the actual company
handbook — with far fewer made-up answers, because the model is told to use only the
retrieved text.

## Run it

```bash
python tutorial/phase2_context_and_memory/module_05_rag/module_5.py
```

Follow the data in the chain: the question goes down two paths at once — into the retriever
(which fetches chunks and formats them as `{context}`) and straight through as `{question}`.
Both land in the prompt, and from there it's the same `prompt | llm | parser` assembly line
you already know. For real files, use loaders like `PyPDFLoader` or `TextLoader` from
`langchain_community.document_loaders`.

## 🏆 Challenge 5 — Add citations

Give each document a `metadata={"source": "..."}` field (split the handbook into two
`Document`s, "handbook-p1" and "handbook-p2"). Change `format_docs` so each chunk is printed
with its source, and update the prompt so the model ends its answer with "Source: ...".

<details><summary><b>Hint</b></summary>

Documents accept metadata:

```python
Document(page_content="...", metadata={"source": "handbook-p1"})
```

In `format_docs`, read it back with `doc.metadata["source"]` and prefix each chunk like
`[handbook-p1] text...`
</details>

Solution: [`solution_5.py`](solution_5.py)
