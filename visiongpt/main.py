import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from chatgpt import visiongpt_response

load_dotenv()

VISION_ANNE_TOKEN=os.getenv("VISION_ANNE_TOKEN")

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print("Forex Anne is ready")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.attachments is not None and message.content is not None:
        await message.channel.send(visiongpt_response(message.attachments[0].url,message.content))

client.run(VISION_ANNE_TOKEN)