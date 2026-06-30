from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import PostgresChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
from vektor_database import search_data_chroma
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(
    # model="gemini-3.5-flash",
    model="gemini-3-flash-preview",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.3
)
SYSTEM_PROMPT = """
Siz professional AI yordamchisiz.

Sizga foydalanuvchi savoli va hujjatlardan topilgan CONTEXT beriladi.

Javob berish qoidalari:

- Faqat CONTEXT asosida javob bering.
- CONTEXT dagi ma'lumotni o'zgartirmang.
- CONTEXT da bir nechta file haqida malumotlar kelib qolsa oldin foydalanuvchidan qaysi fayldan ekanligini so'rang.
- Kerak bo'lsa to'liq iqtibos keltiring.
- Qisqartirmang.
- O'zingizdan ma'lumot qo'shmang.
- Agar javob CONTEXT da mavjud bo'lmasa, aniq ayting:
  "Kechirasiz, berilgan hujjatlar ichida bu ma'lumot topilmadi."

CONTEXT:
{context}
"""
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="rag_chat_history"),
    ("human", "{user_request}")
])

chain = prompt | llm


def save_history_rag_chat(session_id):
    return PostgresChatMessageHistory(
        session_id=session_id,
        connection_string=os.getenv("DATABASE_URL")
    )


chain_with_history = RunnableWithMessageHistory(
    chain,
    save_history_rag_chat,
    input_messages_key="user_request",
    history_messages_key="rag_chat_history"
)


def chat_rag(session_id: str, user_request: str, collection_name):
    context = search_data_chroma(user_request, collection_name)
    response = chain_with_history.invoke({"user_request": user_request, "context": context},
                                         config={"configurable": {"session_id": session_id}})
    return response.content[0]["text"]


