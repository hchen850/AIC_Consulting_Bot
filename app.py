from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage

print("Hello world")
llm = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0,
)

response = llm.invoke([
    HumanMessage(content="Reply with exactly: Mistral connected")
])

print(response.content)
