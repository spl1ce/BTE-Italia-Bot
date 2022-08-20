from calendar import month
from logging import exception
import discord
import emoji
from discord.ext import commands
<<<<<<< Updated upstream
from discord.ext.commands.errors import ChannelNotFound
=======
import datetime
import pytz
import asyncio
>>>>>>> Stashed changes

class Utilities(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot

    @commands.command(name='ping')
    async def ping(self, ctx):
        await ctx.reply(f'Ping! {round((self.bot.latency)*1000, 2)}ms')


    @commands.command(name='post')
    @commands.has_role(701817511284441170)
    async def post(self, ctx, *, links: str):
        link_list = links.split()
        message = '🇮🇹 Nuovo Post!\n🇺🇸 New Post!'
        link_msg = '\n\n'.join(link_list)

        notifiche_channel = self.bot.get_channel(697169688005836810)

        await notifiche_channel.send(f'{message}\n\n{link_msg}')
        
        embed = discord.Embed(description='Posted!', color=discord.Color.green())
        await ctx.send(embed=embed)


    
    @commands.command(name='messaggio')
    @commands.has_role(695697978391789619)
    async def messaggio(self, ctx, channel = None, *, message = None):
        converter = commands.TextChannelConverter()
        
        if channel != None:

            if message != None:
            
                try:
                    destination_channel = await converter.convert(ctx, channel)

                    
                    try:
                        await destination_channel.send(message)

                    except Exception as e:
                        embed = discord.Embed(description="Couldn't send a message to this channel.", color=discord.Color.red())
                        await ctx.send(embed=embed)
                        return

                    embed = discord.Embed(description='Message sent!', color=discord.Color.green())
                    await ctx.send(embed=embed)
                
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
                        embed = discord.Embed(description='Please provide a valid emoji.', color=discord.Color.red())
                        await ctx.send(embed=embed)
                        return

                try:
                    await message.add_reaction(reaction_emoji)
                    

                except Exception as e:
                    print(e)

                    embed = discord.Embed(description="Couldn't react to this message.", color=discord.Color.red())
                    await ctx.send(embed=embed)
                    return
                
                embed = discord.Embed(description='Reacted!', color=discord.Color.green())
                await ctx.send(embed=embed)    

            else:
                embed = discord.Embed(description='You must provide a reaction emoji.', color=discord.Color.red())
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description='You must provide a message.', color=discord.Color.red())
            await ctx.send(embed=embed)




    @commands.command(name='valuta')
    @commands.has_role(756854255662661643)
    async def valuta(self, ctx, post_id = None, minecraft_name = None, points = None):

        if post_id == None or minecraft_name == None or points == None:
            embed = discord.Embed(description=f'Make sure you provide everything like this:\n`{await self.bot.get_prefix(ctx.message)}valuta [POST_ID] [MINECRAFT_USERNAME] [POINTS]`', color=discord.Color.red())
            await ctx.reply(embed=embed)

        else:
            try:
                points = int(points)

            except:
                
                try:
                    points = float(points)
                
                except:
                    embed = discord.Embed(description=f'Points must be a numerical value', color=discord.Color.red())
                    await ctx.send(embed=embed)
                    return
            
            emoji_converter = commands.PartialEmojiConverter()
            verify_emoji = await emoji_converter.convert(ctx, '<:Verified:707278127449112616>')
            
            try:
                channel = await self.bot.fetch_channel(704304928176209940)
                message = await channel.fetch_message(int(post_id))

            except:
                embed = discord.Embed(description=f"I couldn't react to the message.", color=discord.Color.red())
                await ctx.send(embed=embed)
                return

            await message.add_reaction(verify_emoji)

            italiano_role = ctx.guild.get_role(698617888675856514)
            international_role = ctx.guild.get_role(698566163738656909)

            if italiano_role in message.author.roles:
                if int(points) != 1:
                    notification_message = f"Hey *{minecraft_name}*, la tua costruzione è stata valutata **{points} Punti**\nPost di riferimento: https://discord.com/channels/686910132017430538/704304928176209940/{post_id}"
                else:
                    notification_message = f"Hey *{minecraft_name}*, la tua costruzione è stata valutata **{points} Punto**\nPost di riferimento: https://discord.com/channels/686910132017430538/704304928176209940/{post_id}"

            elif international_role in message.author.roles:
                if int(points) != 1:
                    notification_message = f"Hey *{minecraft_name}*, your building has been evaluated **{points} Points**\nReference post: https://discord.com/channels/686910132017430538/704304928176209940/{post_id}"
                else:
                    notification_message = f"Hey *{minecraft_name}*, your building has been evaluated **{points} Point**\nReference post: https://discord.com/channels/686910132017430538/704304928176209940/{post_id}"

            await message.author.send(notification_message)


            try:
                punti_valutazioni = ctx.guild.get_channel(779438755912220713)
                await punti_valutazioni.send(f"{minecraft_name} = {points}")
            
            except:
                embed = discord.Embed(description=f"Couldn't send a message to <#779438755912220713>", color=discord.Color.red())
                await ctx.send(embed=embed)
                return

            confirmation_message = discord.Embed(description=f"Costruzione valutata!", color=discord.Color.green())
            await ctx.reply(embed=confirmation_message)


    async def annouce(self, ctx, deadline, message):
        await discord.utils.sleep_until(deadline)
        print('bababoi')

        channel = ctx.guild.get_channel(696394025921544223)
        await channel.send(message)


    @commands.command(name='riunione')
    #@commands.has_role(756854255662661643)
    async def riunione(self, ctx, *, date=None):
        if date != None:
            try:
                deadline = datetime.datetime.strptime(f"{date} +0100" , "%d/%m/%Y %H:%M %z")
                before_deadline = deadline - datetime.timedelta(minutes=30)
                
                if before_deadline > datetime.datetime.now():
                    
                    message = "<734716661474525244>\nRiunione tra 30 minuti! :bte_italy_animated:"
                    await asyncio.run(await self.annouce(ctx, before_deadline, message))
                
                if deadline > datetime.datetime.now():

                    message = "<734716661474525244>\nRiunione in corso! :bte_italy_animated:"
                    await asyncio.run(await self.annouce(ctx, deadline, message))

            except Exception as e:
                print(e.__str__())
                embed = discord.Embed(
                    description="Sorry, I don't understand it. Please provide the date as follows:\n`£riunione [day/month/year hour:minute]`", 
                    color=discord.Color.red()
                    )
                await ctx.reply(embed=embed)
        
        else:
            embed = discord.Embed(
                description="Please provide the date as follows:\n`£riunione [day/month/year hour:minute]`", 
                color=discord.Color.blue()
                )
            await ctx.reply(embed=embed)


    @post.error
    @messaggio.error
    @reazione.error
<<<<<<< Updated upstream
    async def handler(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            embed = discord.Embed(description="Non hai il permesso di usare questo comando.", color=discord.Color.red())
=======
    @approva.error
    @valuta.error
    async def handler(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            embed = discord.Embed(
                description="Non hai il permesso di usare questo comando.", 
                color=discord.Color.red()
                )
>>>>>>> Stashed changes
            await ctx.send(embed=embed)
        else:
            print(error)

<<<<<<< Updated upstream
def setup(bot):
    bot.add_cog(Utilities(bot))
=======

async def setup(bot):
    await bot.add_cog(Utilities(bot))
>>>>>>> Stashed changes
