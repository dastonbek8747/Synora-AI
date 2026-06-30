from langchain_google_genai import ChatGoogleGenerativeAI
from huggingface_hub import InferenceClient
from google import genai
import urllib.parse
from prompt_image import generate_image_prompt
from dotenv import load_dotenv
import os
import requests
import base64

load_dotenv()


def generate_image_hugging_face(request: str, session_id: str):
    prompt = generate_image_prompt(request)

    client = InferenceClient(
        provider="fal-ai",
        api_key=os.getenv("HUGGINGFACE_API_KEY_6"),
    )

    # output is a PIL.Image object
    image = client.text_to_image(
        prompt,
        model="black-forest-labs/FLUX.1-dev",
    )
    image.save(f"../Users_files/{session_id}/image.png")
    image.show()
    return "rasm saqlandi"


def generate_image_gemini(request: str, session_id: str):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    prompt = generate_image_prompt(request)["prompt_image"]
    response = client.models.generate_content(
        model="imagen-4.0-fast-generate-001",
        contents=[prompt],
    )

    for part in response.parts:
        if part.text is not None:
            print(part.text)

        elif part.inline_data is not None:
            os.makedirs(f"../Users_files/{session_id}")
            image = part.as_image()
            image.save(f"../Users_files/{session_id}/{prompt['image_name']}.png")
            return "rasm saqlandi"
    return "rasm saqlandi"


generate_image_gemini(session_id="dastonz", request="Malika va ristser ajdarho bilan kurashmoqda")


# print(generate_image_gemini("Malika va ritser ajdarho bilan o'rmonda", "daston0778"))


def generate_image_pollinations(request: str, session_id: str):
    prompt = generate_image_prompt(request)
    encode_prompt = urllib.parse.quote(prompt["prompt_image"])
    response = requests.get(
        f"https://image.pollinations.ai/prompt/{encode_prompt}",
        params={"model": "flux"},
        headers={"Authorization": os.getenv("POLLINATIONS_API_KEY")},
    )
    os.makedirs(f"../Users_files/{session_id}")
    with open(f"../Users_files/{session_id}/{prompt['image_name']}.jpg", "wb") as f:
        f.write(response.content)
        return "rasm saqlandi"
