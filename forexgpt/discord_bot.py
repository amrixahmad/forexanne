import discord
from discord.ext import commands
from discord import Interaction
import config as _conf
from chatgpt_app import OpenAIResponse
from cmi_signals import send_signal

class ForexAnneBot:
    def __init__(self, test_mode=True):
        self.client = commands.Bot(command_prefix=".", intents=discord.Intents.all())
        self.chat_response = OpenAIResponse()
        self.forexanne_channel_id = 1202078107046264884
        self.scalping_coach_id = 1199171759392444547
        self.token = _conf.FOREXANNETEST_TOKEN if test_mode else _conf.FOREXANNE_TOKEN

        # Register event handlers
        self.client.event(self.on_ready)
        self.client.event(self.on_message)

        # Register commands
        self.client.tree.command(name="forexanne", description="Send Forex Anne your trade screenshot and question :)")(self.forexanne)
        self.client.tree.command(name="cmi_signals", description="Send signals to any channel")(self.cmi_signals)

    async def on_ready(self):
        try:
            synced = await self.client.tree.sync()
            print(f"{self.client.user.name} is ready")
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)

    async def forexanne(self, interaction: Interaction, trade_ss: discord.Attachment=None, question: str=""):
        if trade_ss is None:
            await self.textanne(interaction, question)
        else:
            await interaction.response.defer()
            image_file = await trade_ss.to_file()
            content = self.chat_response.visiongpt(trade_ss.url, question)
            await interaction.followup.send(content=content, file=image_file)

    async def textanne(self, interaction: Interaction, forex_prompt: str):
        await interaction.response.defer()
        await interaction.followup.send(self.chat_response.chatgpt(forex_prompt))

    async def cmi_signals(self, interaction: Interaction, sl: str, tp1: str, tp2: str, tp3: str, max_tp: str, cl: str, buy: str="", sell: str=""):
        if buy:
            buy_signal = send_signal(sl=sl, tp1=tp1, tp2=tp2, tp3=tp3, max_tp=max_tp, cl=cl, buy=buy)
            await interaction.response.send_message(buy_signal)
        if sell:
            sell_signal = send_signal(sl=sl, tp1=tp1, tp2=tp2, tp3=tp3, max_tp=max_tp, cl=cl, sell=sell)
            await interaction.response.send_message(sell_signal)

    async def on_message(self, message):
        if message.author == self.client.user:
            return
        if message.channel.id in [self.forexanne_channel_id, self.scalping_coach_id]:
            if message.attachments:
                await message.channel.send(self.chat_response.visiongpt(message.attachments[0].url, message.content))
            else:
                await message.channel.send(self.chat_response.chatgpt(message.content))

    def run(self):
        self.client.run(self.token)

