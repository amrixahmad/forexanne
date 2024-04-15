import openai
from prompts.prompts import Prompt
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key=os.getenv("OPENAI_API_KEY")

class OpenAIResponse:
    def __init__(self):
        prompt = Prompt()
        self.base_prompt = prompt.return_base_prompt()
        self.journal_prompt=prompt.return_journal_prompt()

    def visiongpt(self,trade_ss,question=""):
        # prompt = self.base_prompt + question

        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "system",
                    "content": self.base_prompt
                },
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
            max_tokens=500,
            )
        # print(prompt)
        return response.choices[0].message.content

    def journalgpt(self,trade_ss):

        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                "role": "user",
                "content": [
                    {"type": "text", "text": self.journal_prompt},
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

    def chatgpt(self,message):
        prompt = self.base_prompt + message
        completion = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": self.base_prompt
                },
                {"role": "user", "content": prompt}]
            )

        # print(prompt)
        return completion.choices[0].message.content