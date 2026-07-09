"""Module 9 solution — adding a rule-based conciseness evaluator.

Correctness and conciseness often pull in opposite directions — tracking
both is how you notice when a "better" prompt quietly made answers bloated.

To see conciseness fail on purpose: set VERBOSE = True below and rerun,
then compare the two experiments in the LangSmith dashboard.
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langsmith import Client

load_dotenv()
client = Client()

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

VERBOSE = False  # flip to True to watch the conciseness score drop


def my_app(inputs: dict) -> dict:
    style = "Answer in great detail, at least 200 words. " if VERBOSE else ""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    reply = llm.invoke(
        f"{style}Company policy: 24 paid vacation days per year, no rollover.\n"
        f"Question: {inputs['question']}"
    ).content
    return {"answer": reply}


def correctness(outputs: dict, reference_outputs: dict) -> bool:
    judge = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    verdict = judge.invoke(
        f"Reply YES or NO. Does this answer:\n{outputs['answer']}\n"
        f"contain the same facts as this reference:\n{reference_outputs['answer']}"
    ).content
    return "YES" in verdict.upper()


def conciseness(outputs: dict, reference_outputs: dict) -> bool:
    return len(outputs["answer"].split()) < 40


results = client.evaluate(
    my_app,
    data=DATASET,
    evaluators=[correctness, conciseness],
    experiment_prefix="verbose" if VERBOSE else "with-conciseness",
)
