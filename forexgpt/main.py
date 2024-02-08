import discord
from discord.ext import commands
from discord import app_commands
from discord import Interaction
from dotenv import load_dotenv
import asyncio
import os
from chatgpt import visiongpt_response,chatgpt_response

load_dotenv()

FOREXANNE_TOKEN=os.getenv("FOREXANNE_TOKEN")

client = commands.Bot(command_prefix=".",intents=discord.Intents.all())

@client.event
async def on_ready():
    try:
        synced = await client.tree.sync()
        print(f"{client.user.name} is ready")
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

# @client.tree.command(name="forexanne",description="ask Forex Anne anything")
# @app_commands.describe(forex_prompt="Ask me anything about forex")
# async def forexanne(interaction: Interaction,forex_prompt: str):
#     await interaction.response.defer()
#     await asyncio.sleep(delay=6)
#     await interaction.followup.send(chatgpt_response(forex_prompt))

@client.tree.command(name="visionanne",description="send Forex Anne your trade screenshot and question :)")
@app_commands.describe(trade_ss="Send me your trade screenshot and I will analyze it for you. You can also ask me a question about it if you want :)")
async def forexanne(interaction: Interaction,trade_ss: discord.Attachment,question: str="give me a brief summary of this chart based on price action"):
    await interaction.response.defer()
    # await asyncio.sleep(delay=6)    
    image_file = await trade_ss.to_file()
    content = visiongpt_response(trade_ss.url,question)
    await interaction.followup.send(content=content,file=image_file)

client.run(FOREXANNE_TOKEN)