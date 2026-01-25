from fastapi import FastAPI
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(
    model="gpt-4o", # You can also use "gpt-4o-mini" for a cheaper/faster Judge
    temperature=0
)
