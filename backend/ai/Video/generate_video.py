import requests
import urllib.parse
from dotenv import load_dotenv
import os
from .video_prompter import generate_video_prompt

load_dotenv()

API_KEY = os.getenv("POLLINATIONS_API_KEY1")


def generate_video(topic: str, session_id: str):
    prompt = generate_video_prompt(topic)
    prompt_encode = urllib.parse.quote(prompt['prompt_video'])
    response = requests.get(
        f"https://gen.pollinations.ai/video/{prompt_encode}",
        params={"model": "wan-fast", "duration": 5},
        headers={"Authorization": f"Bearer {API_KEY}"},
    )
    print(response.text, response.status_code)
    os.makedirs(f"./Users_files/{session_id}", exist_ok=True)
    with open(f"./Users_files/{session_id}/{prompt['video_name']}.mp4", "wb") as f:
        f.write(response.content)
        return {"message": "video saqlandi", "video_name": prompt['video_name'],
                "video_path": f"{session_id}/{prompt['video_name']}.mp4"}


# print(generate_video("Cristiano speaking siuuuuu  !", "65a69163-037b-4e34-bbd3-1d5344cf0007"))
