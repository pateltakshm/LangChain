# Module 2 — Prompt Templates

## The idea

In Module 1 you wrote the prompt by hand. Real apps need prompts that are **reusable**: the
wording stays the same, but pieces of it (the user's question, the language, the tone) change
every time. A **prompt template** is a prompt with labeled blanks, like `{language}`, that
you fill in at runtime.

> **Mental model:** a prompt template is a *form letter*. A bank does not write every letter
> from scratch — it keeps one letter with blanks: "Dear *[name]*, your balance is
> *[amount]*." Templates also let you set a **system message**: standing instructions that
> tell the model who it is, before the user says anything.

## Real-world use case

A travel app translates user reviews into many languages. The instruction ("translate this,
keep the tone") never changes — only the language and the text do. One template serves
millions of requests.

## Run it

```bash
python tutorial/phase1_building_blocks/module_02_prompt_templates/module_2.py
```

Notice that `prompt.invoke()` and `llm.invoke()` have the same shape — everything in
LangChain is a component you can invoke. That symmetry is what makes chains possible in the
next module.

## 🏆 Challenge 2 — Build a recipe generator template

Create a template with three variables: `{ingredient}`, `{diet}` (e.g. "vegan"), and
`{minutes}` (maximum cooking time). The system message should make the model a friendly chef
who always lists ingredients first, then numbered steps. Test it with two different inputs.

<details><summary><b>Hint</b></summary>

Put the persona and the output-format rules in the `system` message. The `human` message can
be short, like `"Give me a {diet} recipe using {ingredient} that takes under {minutes} minutes."`
</details>

Solution: [`solution_2.py`](solution_2.py)
