import discord
from discord.ext import commands
import asyncio

# Define intents
intents = discord.Intents.default()
intents.messages = True  # Enable message events

# Initialize your Discord bot with intents
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Logged in as', bot.user.name)

@bot.command()
async def hello(ctx):
    # Send "Hello!" to the Discord channel where the command was issued
    await ctx.send('Hello!')

# Run your Discord bot with the event loop specified
loop = asyncio.get_event_loop()
asyncio.run(bot.start('MTIwNDQ0ODgyMTA5MDk4Mzk2Nw.GJpRE4.zach0LbiBoqeVLSBRDBcutxAqiKrFqC-5yIaMI'))
