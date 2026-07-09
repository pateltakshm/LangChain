"""Module 1 solution — Support Draft bot, comparing temperatures.

Run it a few times: the temperature=0 reply barely changes, while the
temperature=1 reply is different each run. Use low temperature for factual
tasks, higher for creative ones.
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

complaint = "My package arrived two weeks late and the box was damaged."

prompt = (
    "Write a short, apologetic customer-support reply to this complaint. "
    f"Offer a refund. Complaint: {complaint}"
)

focused_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
creative_llm = ChatOpenAI(model="gpt-4o-mini", temperature=1)

print("--- temperature=0 (same every run) ---")
print(focused_llm.invoke(prompt).content)

print("\n--- temperature=1 (varies every run) ---")
print(creative_llm.invoke(prompt).content)
