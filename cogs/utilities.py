import discord
import emoji
from discord.ext import commands
from discord.ext.commands.errors import ChannelNotFound

class Utilities(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot

    @commands.command(name='post')
    @commands.has_role(701817511284441170)
    async def post(self, ctx, *, links: str):
        link_list = links.split()
        message = '🇮🇹 Nuovo Post!\n🇺🇸 New Post!'
        link_msg = '\n\n'.join(link_list)

        notifiche_channel = self.bot.get_channel(697169688005836810)

        await notifiche_channel.send(f'{message}\n\n{link_msg}')

    
    @commands.command(name='messaggio')
    @commands.has_role(695697978391789619)
    async def messaggio(self, ctx, channel = None, *, message = None):
        converter = commands.TextChannelConverter()
        
        if channel != None:

            if message != None:
            
                try:
                    destination_channel = await converter.convert(ctx, channel)

                    embed = discord.Embed(description='Message sent!', color=discord.Color.green())
                    await destination_channel.send(message)

                except commands.ChannelNotFound:
                    embed = discord.Embed(description='Channel not found.', color=discord.Color.red())
                    await ctx.send(embed=embed)

            else:
                embed = discord.Embed(description='Please provide a valid message.', color=discord.Color.red())
                await ctx.send(embed=embed)
        
        else:
            embed = discord.Embed(description='You must provide a channel.', color=discord.Color.red())
            await ctx.send(embed=embed)
    
    @commands.command(name='reazione')
    @commands.has_role(695697978391789619)
    async def reazione(self, ctx, message = None, reaction = None):
        if message != None:
        
            if reaction != None:
                reaction_message = None
                try:
                    message_converter = commands.MessageConverter()
                    reaction_message = await message_converter.convert(ctx, message)

                except commands.MessageNotFound:
                    channels = ctx.guild.channels
                    for channel in channels:
                        try:
                            reaction_message = await channel.fetch_message(message)

                        except:
                            pass

                    if reaction_message == None:
                        embed = discord.Embed(description="Couldn't find the message.", color=discord.Color.red())
                        await ctx.send(embed=embed)
                        return

                if reaction in emoji.UNICODE_EMOJI_ENGLISH:
                    reaction_emoji = reaction

                else:
                    try:
                        emoji_converter = commands.PartialEmojiConverter()
                        reaction_emoji = await emoji_converter.convert(ctx, reaction)
                        


                    except commands.PartialEmojiConversionFailure:
                        embed=discord.Embed(description='Please provide a valid emoji.', color=discord.Color.red())
                        await ctx.send(embed=embed)
                        return

                await message.add_reaction(reaction_emoji)
                

            else:
                embed = discord.Embed(description='You must provide a reaction emoji.', color=discord.Color.red())
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description='You must provide a message.', color=discord.Color.red())
            await ctx.send(embed=embed)



    @post.error
    @messaggio.error
    @reazione.error
    async def handler(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            embed = discord.Embed(description="Non hai il permesso di usare questo comando.", color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            print(error)

def setup(bot):
    bot.add_cog(Utilities(bot))
