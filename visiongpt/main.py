import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from chatgpt import visiongpt_response,chatgpt_response

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
    
    if message.attachments:
        await message.channel.send(visiongpt_response(message.attachments[0].url,message.content))
    
    else:
        await message.channel.send(chatgpt_response(message.content))

client.run(VISION_ANNE_TOKEN)