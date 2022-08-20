import discord
from discord.ext import commands
from datetime import datetime

from discord.ext.commands.core import after_invoke

class Mute(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        author = message.author
        channel = message.channel
        messages = []

        async for message in channel.history(limit=50):
            if message.author == author:
                messages.append(message)
            else:
                pass
        if len(messages) >= 5:
            msg_1_time = messages[0].created_at
            msg_5_time = messages[4].created_at

            difference = (msg_1_time - msg_5_time)

            total_seconds = difference.total_seconds()
            if total_seconds <= 4:
                print('3')
                await message.channel.send('ok')
                print('okokokokok')



def setup(bot):
    bot.add_cog(Mute(bot))