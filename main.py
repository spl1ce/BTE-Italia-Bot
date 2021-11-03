import discord
import os
from discord.ext import commands

intents=discord.Intents.all()
intents.reactions=True
intents.messages=True

bot = commands.Bot(command_prefix='+', intents=intents)

async def run_once_when_ready():
    await bot.wait_until_ready()
    print('BTE Italia Bot In Funzione!')
    await bot.change_presence(activity=discord.Activity(type = discord.ActivityType.watching,name='www.bteitalia.it'))


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

    else:
        print(f'Unable to load {filename}.')

bot.loop.create_task(run_once_when_ready())
bot.run(os.environ.get('TOKEN'))