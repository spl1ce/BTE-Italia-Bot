import discord
import os
from discord.ext import commands

bot = commands.Bot(command_prefix='£')

@bot.event
async def on_connect():
    print('Bot is ready!')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


bot.run('ODc1MjkzNDA3OTY5NDI3NTE4.YRTagg.59qiBctr7wDaVjXw0hTRtX6zkYs')