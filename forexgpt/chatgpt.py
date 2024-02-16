import openai
from prompts import Prompt
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key=os.getenv("OPENAI_API_KEY")

prompt = Prompt()
base_prompt = prompt.return_base_prompt()

def visiongpt_response(trade_ss,question=base_prompt):
    prompt = base_prompt + question

    response = openai.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                "type": "image_url",
                "image_url": {
                    "url": trade_ss,
                },
                },
            ],
            }
        ],
        max_tokens=500,
        )
    # print(prompt)
    return response.choices[0].message.content

def chatgpt_response(message):
    prompt = base_prompt + message
    completion = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
        )

    # print(prompt)
    return completion.choices[0].message.content