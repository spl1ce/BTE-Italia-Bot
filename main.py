import discord
import os
import asyncio

intents=discord.Intents.all()
intents.reactions=True
intents.messages=True

class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self):

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await bot.load_extension(f"cogs.{filename[:-3]}")
                logging.info(f"{filename} caricato!")

            else:
                logging.error(f"Unable to load {filename}.")
    
    async def on_ready(self):
        print('BTE Italia Bot In Funzione!')


bot = MyBot(command_prefix='&', intents=intents, activity=discord.Activity(type=discord.ActivityType.watching, name='bteitalia.it'))


bot.run('MTAwNzQxMDYzNTk5NjQxNDAxMg.G2lQL9.zEhmYxkI4hcO7JfV_H6YbSYNS6UP9BgLGAieto')