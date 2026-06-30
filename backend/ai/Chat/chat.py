from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import psycopg
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_postgres import PostgresChatMessageHistory
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.prompts import ChatPromptTemplate
import os
from uuid import uuid4

session_id = str(uuid4())
load_dotenv()

conn = psycopg.connect(os.getenv("DATABASE_URL"))
PostgresChatMessageHistory.create_tables(conn, "chat_history")

model1 = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    api_key=os.getenv("GEMINI_API_KEY"),
)

prompt = ChatPromptTemplate.from_messages([
    ('system',
     "Siz aqlli dastur yordamchisiz. Foydalanuvchi bilan har doim UZBEK tilida muloqot qiling. Foydalanuvchi siz bilan muloqot qiladi. Foydalanuvchi bilan hushmuomila bo'ling. Foydalanuvchi savollariga aniq va to'liq javob bering."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{user_request}")
])


def get_chat_history(session_id: str):
    return PostgresChatMessageHistory("chat_history", session_id, sync_connection=conn)


chain = prompt | model1

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_chat_history,
    input_messages_key="user_request",
    history_messages_key="chat_history"
)


def chat_with_model(request: str):
    response = chain.invoke({"user_request": request})
    return response.content[0]["text"]


def chat_with_history_model(request: str, session_id: str):
    response = chain_with_history.invoke({"user_request": request}, config={"configurable": {"session_id": session_id}})
    print(response.content[0]["text"])


chat_with_history_model(request="Salom !", session_id=session_id)
