# The LangChain Path — Beginner to Expert

A hands-on, 9-module course. Every module folder contains:

| File | What it is |
|---|---|
| `README.md` | The concept explained simply, a real-world use case, and a practice challenge (with a hint) |
| `module_X.py` | The runnable walkthrough code — read it, run it, tweak it |
| `solution_X.py` | Full solution to the challenge — only open after trying! |

## Curriculum

**Phase 1 — The Building Blocks (Complete Beginner)**
1. [LLMs and LangChain](phase1_building_blocks/module_01_llms_and_langchain/) — your first completion
2. [Prompt Templates](phase1_building_blocks/module_02_prompt_templates/) — reusable prompts with blanks
3. [Simple Chains (LCEL)](phase1_building_blocks/module_03_simple_chains/) — the `prompt | model | parser` assembly line

**Phase 2 — Context and Memory (Intermediate)**
4. [Chat History & Memory](phase2_context_and_memory/module_04_memory/) — bots that remember
5. [RAG](phase2_context_and_memory/module_05_rag/) — talk to your own documents

**Phase 3 — Agents and Tools (Advanced)**
6. [Tools & Function Calling](phase3_agents_and_tools/module_06_tools/) — give the LLM hands
7. [ReAct Agents](phase3_agents_and_tools/module_07_react_agents/) — think, act, observe, repeat

**Phase 4 — Production (Expert)**
8. [LangGraph](phase4_production/module_08_langgraph/) — cyclical workflows and state machines
9. [Evaluation & LangSmith](phase4_production/module_09_langsmith/) — trace, debug, and score

## One-time setup

From the repo root (`LangChain/`):

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file **in the repo root** (copy `.env.example`) and put your key in it:

```
OPENAI_API_KEY=sk-your-key-here
```

Get a key at <https://platform.openai.com>. Modules 7–8 need `langgraph`, Module 9 needs
`langsmith` — both are already in `requirements.txt`.

## How to run any module

Always run from the **repo root** so `.env` is found:

```bash
python tutorial/phase1_building_blocks/module_01_llms_and_langchain/module_1.py
```

## How to study

1. Read the module's `README.md`.
2. Run `module_X.py`, then change something small and run it again.
3. Attempt the challenge on your own. Peek at the hint if stuck.
4. Compare with `solution_X.py`.

Happy chaining. `prompt | model | you`
