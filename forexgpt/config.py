from dotenv import load_dotenv
import os

load_dotenv()

FOREXANNETEST_TOKEN=os.getenv("FOREXANNETEST_TOKEN")
FOREXANNE_TOKEN=os.getenv("FOREXANNE_TOKEN")
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
METALAPI_API_KEY=os.getenv("METALAPI_API_KEY")