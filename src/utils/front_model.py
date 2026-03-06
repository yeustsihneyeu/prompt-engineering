import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

openai = OpenAI()

def openai_generate(prompt: str):
    response = openai.responses.create(
        model="gpt-4.1",
        input=prompt
    )
    return response.output_text