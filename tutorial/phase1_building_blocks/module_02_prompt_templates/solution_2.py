"""Module 2 solution — recipe generator template.

One template, endless recipes. This separation — fixed instructions,
changing data — is the single most important habit in prompt engineering.
"""

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.8)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a friendly chef. Always answer with two sections: "
               "'Ingredients' as a bullet list, then 'Steps' as a numbered list. "
               "Keep recipes simple for home cooks."),
    ("human", "Give me a {diet} recipe using {ingredient} "
              "that takes under {minutes} minutes."),
])

for inputs in [
    {"ingredient": "chickpeas", "diet": "vegan", "minutes": 20},
    {"ingredient": "salmon", "diet": "keto", "minutes": 30},
]:
    messages = prompt.invoke(inputs)
    print(f"\n===== {inputs['diet']} / {inputs['ingredient']} =====")
    print(llm.invoke(messages).content)
