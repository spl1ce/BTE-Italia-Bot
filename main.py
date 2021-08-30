import discord
import os
from discord.ext import commands

bot = commands.Bot(command_prefix='£')

async def run_once_when_ready():
    await bot.wait_until_ready()
    print('BTE Italia Bot In Funzione!')
    await bot.change_presence(activity=discord.Activity(type = discord.ActivityType.watching,name='www.bteitalia.it'))


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


bot.loop.create_task(run_once_when_ready())
bot.run('ODc1MjkzNDA3OTY5NDI3NTE4.YRTagg.59qiBctr7wDaVjXw0hTRtX6zkYs')
