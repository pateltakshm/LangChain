"""Module 9 — Scoring your app against a test set with LangSmith.

Requires LANGSMITH_API_KEY in your .env (free account at smith.langchain.com).
Results appear in the LangSmith dashboard under 'hr-bot-tests'.
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langsmith import Client

load_dotenv()
client = Client()

# 1. A test set: questions with known good answers (created once, reused after)
DATASET = "hr-bot-tests"
if not client.has_dataset(dataset_name=DATASET):
    dataset = client.create_dataset(DATASET)
    client.create_examples(
        dataset_id=dataset.id,
        examples=[
            {"inputs": {"question": "How many vacation days do full-time employees get?"},
             "outputs": {"answer": "24 paid vacation days per year"}},
            {"inputs": {"question": "Do unused vacation days roll over?"},
             "outputs": {"answer": "No, unused days do not roll over"}},
        ],
    )


# 2. The app being tested (imagine your Module 5 RAG chain here)
def my_app(inputs: dict) -> dict:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    reply = llm.invoke(
        "Company policy: 24 paid vacation days per year, no rollover.\n"
        f"Question: {inputs['question']}"
    ).content
    return {"answer": reply}


# 3. An evaluator: scores each answer against the expected one (LLM-as-judge)
def correctness(outputs: dict, reference_outputs: dict) -> bool:
    judge = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    verdict = judge.invoke(
        f"Reply YES or NO. Does this answer:\n{outputs['answer']}\n"
        f"contain the same facts as this reference:\n{reference_outputs['answer']}"
    ).content
    return "YES" in verdict.upper()


# 4. Run the experiment — results appear in the LangSmith dashboard
results = client.evaluate(
    my_app,
    data=DATASET,
    evaluators=[correctness],
    experiment_prefix="baseline",
)
