import discord
import emoji
from discord.ext import commands
from os import environ
from utils.spreadsheet import Spreadsheet
from asyncio import sleep

sh = Spreadsheet(environ.get('SPREADSHEET_ID'))


async def refresh_spreadsheet():
    while True:
        sh.fetch()
        await sleep(10800)  # 3 hours


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
        
        embed = discord.Embed(description='Postato!', color=discord.Color.green())
        await ctx.send(embed=embed)


    
    @commands.command(name='messaggio')
    @commands.has_role(695697978391789619)
    async def messaggio(self, ctx, channel = None, *, message = None):
        converter = commands.TextChannelConverter()
        
        if channel != None:

            if message != None or ctx.message.attachments != None:
            
                try:
                    destination_channel = await converter.convert(ctx, channel)

                    
                    try:
                        attachments = ctx.message.attachments
                        files = []                        
                        for file in attachments:
                            files.append(await file.to_file())    
                        
                        await destination_channel.send(content=message, files=files)

                    except Exception as e:
                        embed = discord.Embed(description="Non è stato possibile mandare un messaggio a questo canale.", color=discord.Color.red())
                        await ctx.send(embed=embed)
                        print(e)
                        return

                    embed = discord.Embed(description='Messaggio inviato!', color=discord.Color.green())
                    await ctx.send(embed=embed)
                
                except commands.ChannelNotFound:
                    embed = discord.Embed(description='Canale non trovato.', color=discord.Color.red())
                    await ctx.send(embed=embed)

            else:
                embed = discord.Embed(description='Perfavore invia un messaggio valido.', color=discord.Color.red())
                await ctx.send(embed=embed)
        
        else:
            embed = discord.Embed(description='Devi indicare un canale.', color=discord.Color.red())
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
                        embed = discord.Embed(description="Non è stato possibile trovare il messaggio.", color=discord.Color.red())
                        await ctx.send(embed=embed)
                        return

                if reaction in emoji.UNICODE_EMOJI_ENGLISH:
                    reaction_emoji = reaction

                else:
                    try:
                        emoji_converter = commands.PartialEmojiConverter()
                        reaction_emoji = await emoji_converter.convert(ctx, reaction)
                        


                    except commands.PartialEmojiConversionFailure:
                        embed = discord.Embed(description='Perfavore indica un emoji valida.', color=discord.Color.red())
                        await ctx.send(embed=embed)
                        return

                try:
                    await reaction_message.add_reaction(reaction_emoji)
                    

                except Exception as e:
                    print(e)

                    embed = discord.Embed(description="Non è stato possibile reagire al messaggio.", color=discord.Color.red())
                    await ctx.send(embed=embed)
                    return
                
                embed = discord.Embed(description='Reagito!', color=discord.Color.green())
                await ctx.send(embed=embed)    

            else:
                embed = discord.Embed(description='Devi indicare un emoji da reagire.', color=discord.Color.red())
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description='Devi indicare un messaggio.', color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command(name='approva')
    @commands.has_role(704338128692838533)
    async def approva(self, ctx, member = None):
        approva_channel = ctx.guild.get_channel(891675282992431154)
        if ctx.channel == approva_channel:
            if member != None:
                try:
                    converter=commands.MemberConverter()
                    member = await converter.convert(ctx, member)

                    starter_role = ctx.guild.get_role(704332197628477450)
                    if not starter_role in member.roles:
                        try:
                            newbie_role = ctx.guild.get_role(884464061851521065)
                            await member.remove_roles(newbie_role)
                            
                        except Exception as e:
                            print(e)
                            embed=discord.Embed(description="Non è stato possibile rimuovere il ruolo Newbie dal utente.", color=discord.Color.red())
                            await ctx.send(embed=embed)
                            return

                        try:
                            starter_role = ctx.guild.get_role(704332197628477450)
                            await member.add_roles(starter_role)


                        except Exception as e:
                            print(e)
                            embed=discord.Embed(description="Rimosso il ruolo Newbie ma non è stato posssibile assegnare Starter.", color=discord.Color.red())
                            await ctx.send(embed=embed)
                            return

                        # Search for the user in the sheets
                        applicationsList = sh.get()
                        minecraftName = ""
                        for application in applicationsList:
                            #      v-- Discord name + discriminator
                            if application[2] == f"{member.name}#{member.discriminator}":
                                # Minecraft In game name
                                minecraftName = application[1]

                        if minecraftName == "":
                            embed = discord.Embed(
                                description="{member.name}#{member.discriminator} è stato approvato su Discord ma non su Minecraft, per favore contatta il <@&696409124102996068>.", color=discord.Color.gold())
                            await ctx.send(embed=embed)
                        else:
                            # Send lp command to the console channel
                            console_channel = ctx.guild.get_channel(
                                778281056284442664)

                            await console_channel.send(f"lp user {minecraftName} group add starter")

                            embed = discord.Embed(
                                description=f"Approvato {member.name}#{member.discriminator}!", color=discord.Color.green())
                            await ctx.send(embed=embed)

                    else:
                        embed = discord.Embed(description='Utente ha già il ruolo Starter.', color=discord.Color.red())
                        await ctx.send(embed=embed)

                except commands.MemberNotFound:
                    embed = discord.Embed(description='Utente non trovato!', color=discord.Color.red())
                    await ctx.send(embed=embed)
                    return

            else:
                embed = discord.Embed(description='Devi indicare un Utente!', color=discord.Color.red())
                await ctx.send(embed=embed)

        else:
            pass

    @post.error
    @messaggio.error
    @reazione.error
    @approva.error
    async def handler(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            embed = discord.Embed(description="Non hai il permesso di usare questo comando.", color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            print(error)


def setup(bot):
    bot.add_cog(Utilities(bot))
    bot.loop.create_task(refresh_spreadsheet())
