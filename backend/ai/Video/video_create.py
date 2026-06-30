import os
from huggingface_hub import InferenceClient
import requests
from video_prompt import generate_video_prompt
from dotenv import load_dotenv

load_dotenv()


def generate_video(request: str):
    response = requests.get(
        "https://gen.pollinations.ai/video/a sunset timelapse",
        params={"model": "veo", "duration": 4},
        headers={"Authorization": os.getenv("POLLINATIONS_API_KEY")},
    )
    with open("video.mp4", "wb") as f:
        f.write(response.content)
    return "video.mp4"


print(generate_video("crate children feed"))


def generate_video_hugging_face(request: str):
    prompt = generate_video_prompt(request)
    client = InferenceClient(
        provider="fal-ai",
        api_key=os.getenv("huggingface_api_key_5"),
    )
    video = client.text_to_video(
        prompt,
        model="Wan-AI/Wan2.2-TI2V-5B",
    )
    with open("video.mp4", "wb") as f:
        f.write(video)
    print("video saqlandi")

# generate_video("Amazonka o'rmonida momaqaldiroq — chaqmoqlar va yomg'ir")
# generate_video_hugging_face("Amazonka o'rmonida momaqaldiroq - chaqmoqlar va yomg'ir")
