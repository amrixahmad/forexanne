import discord
from discord.ext import commands
from discord import app_commands
from discord import Interaction
from dotenv import load_dotenv
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

async def textanne(interaction: Interaction,forex_prompt: str):
    await interaction.response.defer()
    await interaction.followup.send(chatgpt_response(forex_prompt))

@client.tree.command(name="forexanne",description="send Forex Anne your trade screenshot and question :)")
@app_commands.describe(trade_ss="Send me your trade screenshot and I will analyze it for you. You can also ask me a question about it if you want :)")
async def forexanne(interaction: Interaction,trade_ss: discord.Attachment=None,question: str="give me a brief summary of this chart based on price action"):
    
    if trade_ss is None:
        await textanne(interaction=interaction,forex_prompt=question)
    
    else:
        await interaction.response.defer()
        image_file = await trade_ss.to_file()
        content = visiongpt_response(trade_ss.url,question)
        await interaction.followup.send(content=content,file=image_file)

client.run(FOREXANNE_TOKEN)