import openai
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key=os.getenv("OPENAI_API_KEY")

def visiongpt_response(trade_ss,question):
    response = openai.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
            "role": "user",
            "content": [
                {"type": "text", "text": question},
                {
                "type": "image_url",
                "image_url": {
                    "url": trade_ss,
                },
                },
            ],
            }
        ],
        max_tokens=2000,
        )

    return response.choices[0].message.content