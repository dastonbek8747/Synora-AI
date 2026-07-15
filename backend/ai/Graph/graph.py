from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from typing import Literal, TypedDict, List
from pydantic import BaseModel, Field
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", api_key=os.getenv("GEMINI_API_KEY"))


class llm_schema(BaseModel):
    chat_content: Literal["chat", "create_image", "search", "create_video", "rag", "writer_ai"] = Field(...,
                                                                                                        description="Berilgan matinni mazmuni analiz qilib foydalanuvchi istagiga mos javobni response qiling")


schema = llm_with_structed = llm.with_structured_output(llm_schema)
print(schema.invoke("Menga 'Uzbekiston' mavzusida inshoga rasim chizing. "))


class schema_graph(TypedDict):
    chat_user_messages: str
    chat_content: str
    response_ai: dict[str, str]
