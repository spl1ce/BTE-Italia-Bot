import discord
import time
from discord.ext import commands
import asyncio

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='clear', description='Elimina la quantità di messaggi forniti.')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        limit=100
        if 1 <= amount <= limit:
            await ctx.channel.purge(limit=amount+1)
            embed=discord.Embed(description=f'Cancellati {amount} messaggi.', color=discord.Color.green())
            message = await ctx.channel.send(embed=embed)
            time.sleep(10)
            await message.delete()

        else:
            embed=discord.Embed(description='Perfavore inserisci un numero tra `0-100`.', color=discord.Color.red())
            await ctx.channel.send(embed=embed)

    @clear.error
    async def handler(self, ctx, error):
        if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(description='Perfavore inserisci un numero valido tra `0-100`.', color=discord.Color.red())
            await ctx.channel.send(embed=embed)
        else:
            print(error)
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def banlist(self, ctx):
        page = 1
        bans = await ctx.guild.bans()

        def check(reaction, user):
            return user != self.client.user
        message = None

        while True:
            header = f"Lista Utenti Bannati (Pagina #{page}):"
            embed = discord.Embed(
                title=f"{header}", color=discord.Color.blue())
            for ban_entry in bans[(page-1)*10:page*10]:
                embed.add_field(
                    name=f"**{ban_entry.user}**", value=f"Motivo: *{ban_entry.reason}*")
            if message == None:
                message = await ctx.send(embed=embed)
            else:
                await message.edit(embed=embed)
            if len(bans) > 10 and not page*10 - len(bans) <= 10:
                await message.add_reaction("◀️")
                await message.add_reaction("▶️")
                try:
                    reaction, user = await self.client.wait_for('reaction_add', timeout=30.0, check=check)
                except asyncio.TimeoutError:
                    await message.clear_reaction("◀️")
                    await message.clear_reaction("▶️")
                    break
                if str(reaction) == "▶️":
                    page += 1
                elif str(reaction) == "◀️" and page > 1:
                    page -= 1
                else:
                    print("none of the reactions")
            else:
                break

    @banlist.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description='Non hai il permesso di eseguire questo comando',
                colour=discord.Colour.red()
            )
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, *, reason=None):
        if member == None:
            embed = discord.Embed(
                description=':x: Perfavore specifica un utente da bannare', color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            await member.ban(reason=reason)
            embed = discord.Embed(
                description='✅ Bannato {} per ``{}``'.format(
                    member.mention, reason),
                colour=discord.Colour.green()
            )

            await ctx.send(embed=embed)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description='Non hai il permesso di eseguire questo comando',
                colour=discord.Colour.red()
            )
            await ctx.send(embed=embed)
            
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member=None):
        if member == None:
            embed = discord.Embed(
                description=':x: Perfavore specifica un utente da sbannare', color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split('#')

            for ban_entry in banned_users:
                user = ban_entry.user

                if(user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    embed = discord.Embed(
                        description='✅ Sbannato {}'.format(
                            user.mention),
                        colour=discord.Colour.green()
                    )
                    await ctx.send(embed=embed)
                    return

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description='Non hai il permesso di usare questo comando',
                colour=discord.Colour.red()
            )
            await ctx.send(embed=embed)
            
def setup(bot):
    bot.add_cog(Moderation(bot))
