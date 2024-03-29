import discord
from discord.ext import commands
from discord import app_commands
from discord import Interaction
from discord import AllowedMentions
from dotenv import load_dotenv
import os
from chatgpt import OpenAIResponse
from cmi_signals import send_signal
from gdrive.dailytrades import DailyTrades,channel_ids,test_channel_ids
from gdrive.sheetsauth import SheetsAuth,SCOPES

load_dotenv()

forexanne_channel_id=1202078107046264884
scalping_coach_id=1199171759392444547

def is_test(test=bool):
    FOREXANNETEST_TOKEN=os.getenv("FOREXANNETEST_TOKEN")
    FOREXANNE_TOKEN=os.getenv("FOREXANNE_TOKEN")
    if test:
        return FOREXANNETEST_TOKEN
    else:
        return FOREXANNE_TOKEN

client = commands.Bot(command_prefix=".",intents=discord.Intents.all())
chat_response=OpenAIResponse()

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
    await interaction.followup.send(chat_response.chatgpt(forex_prompt))

@client.tree.command(name="forexanne",description="send Forex Anne your trade screenshot and question :)")
@app_commands.describe(trade_ss="Send me your trade screenshot and I will analyze it for you. You can also ask me a question about it if you want :)")
@app_commands.describe(question="Ask me anything about forex price action trading :)")
async def forexanne(interaction: Interaction,trade_ss: discord.Attachment=None,question: str=""):
    
    if trade_ss is None:
        await textanne(interaction=interaction,forex_prompt=question)
    
    else:
        await interaction.response.defer()
        image_file = await trade_ss.to_file()
        content = chat_response.visiongpt(trade_ss.url,question)
        await interaction.followup.send(content=content,file=image_file)

@client.tree.command(name="cmi_signals",description="send signals to any channel")
async def cmi_signals(    
    interaction: Interaction,
    sl: str,
    tp1: str,
    tp2: str,
    tp3: str,
    max_tp: str,
    cl: str,
    buy: str="",
    sell: str=""
    ):
    # mention_everyone=AllowedMentions(everyone=True)
    if buy:
        buy_signal=send_signal(sl=sl,tp1=tp1,tp2=tp2,tp3=tp3,max_tp=max_tp,cl=cl,buy=buy)        
        await interaction.response.send_message(buy_signal)
    if sell:
        sell_signal=send_signal(sl=sl,tp1=tp1,tp2=tp2,tp3=tp3,max_tp=max_tp,cl=cl,sell=sell)
        await interaction.response.send_message(sell_signal)

async def journal_gpt(message,channel_ids):
    if any(d['value'] == message.channel.id for d in channel_ids if 'value' in d):
        daily_trades=DailyTrades(creds=SheetsAuth(scopes=SCOPES).authorize())
        # Get channel ID and name
        channel_id = message.channel.id
        channel_name = message.channel.name
        # await message.channel.send(message.channel.name)
        if message.attachments:
            # await message.channel.send(message.channel.name)
            for attachment in message.attachments:
                if any(attachment.filename.lower().endswith(image_ext) for image_ext in ['.png', '.jpg', '.jpeg', '.gif','.webp']):
                    # Upload to Google Drive
                    file_id,link=daily_trades.upload_image_from_url(attachment.url)
                    journal_entry=chat_response.journalgpt(message.attachments[0].url)
                    daily_trades.add_student_roadmap_row(
                        str(message.author),
                        str(channel_id),
                        channel_name,
                        file_id,
                        link,  # Link to the uploaded file
                        journal_entry
                    )
                    await message.channel.send(f"Thank you, {message.author} I have written a journal entry for you :)")

@client.event
async def on_message(message):
    
    if message.author==client.user:
        return

    if message.channel.id==forexanne_channel_id or message.channel.id==scalping_coach_id:
        # print(message.content)
        # print(message.channel.id)
        if message.attachments:
            await message.channel.send(chat_response.visiongpt(message.attachments[0].url,message.content))
        else:
            await message.channel.send(chat_response.chatgpt(message.content))

    await journal_gpt(message=message,channel_ids=test_channel_ids)
    

client.run(is_test(test=False))