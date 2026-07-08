import requests
import uuid


# user_id = uuid.uuid4()
def chat_ai(request: str, session_id: str):
    response = requests.post(url="http://127.0.0.1:8000/chat",
                             params={"message": request, "session_id": str(session_id)})

    return response.json()
