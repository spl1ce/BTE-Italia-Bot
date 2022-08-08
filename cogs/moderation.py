import discord
import time
from discord.ext import commands
import asyncio
import time
import pymongo
import os
import re
from datetime import datetime
from discord.utils import get
import math
import json

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='clear', description='Elimina la quantità di messaggi forniti.')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        limit=100
        if 1 <= amount <= limit:
            await ctx.channel.purge(limit=amount+1)
            embed=discord.Embed(description=f':wastebasket: Cancellati {amount} messaggi.', color=discord.Color.green())
            message = await ctx.channel.send(embed=embed)
            time.sleep(10)
            await message.delete()

        else:
            embed=discord.Embed(description=':x: Perfavore inserisci un numero tra `0-100`.', color=discord.Color.red())
            await ctx.channel.send(embed=embed)

    @clear.error
    async def handler(self, ctx, error):
        if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(description=':x: Perfavore inserisci un numero valido tra `0-100`.', color=discord.Color.red())
            await ctx.channel.send(embed=embed)
        else:
            print(error)
    
    @commands.command(name='banlist', description='Fornirà la lista degli utenti bannati.')
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

    @commands.command(name='ban', description='Bannerà dal server il utente specificato.')
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
            
    @commands.command(name='unban', description='Sbannerà dal server il utente specificato.')
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
            
    @commands.command(name='kick', description='Kickerà dal server il utente specificato.')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, *, reason=None):
        if member == None:
            embed = discord.Embed(
                description=':x: Perfavore specifica un utente da kickare', color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            await member.kick(reason=reason)
            embed = discord.Embed(
                description='✅ Kickato {} per ``{}``'.format(
                    member.mention, reason),
                colour=discord.Colour.green()
            )
            await ctx.send(embed=embed)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description='Non hai il permesso di eseguire questo comando',
                colour=discord.Colour.red()
            )
            await ctx.send(embed=embed)
           
    @commands.command(name='userinfo', description='Fornirà informazioni di un utente.')
    async def userinfo(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        embed = discord.Embed(
            color=discord.Color.orange(),
            timestamp=ctx.message.created_at
        )
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_author(
            name=f'Informazioni su: {member.display_name}'
        )
        embed.add_field(
            name=':bust_in_silhouette: Informazioni Account',
            value=f":signal_strength: Attualmente {member.status}\n:beginner: Creato il {member.created_at.strftime('%d %b %Y %H:%M')}",
            inline=False
        )
        if member.premium_since == None:
            embed.add_field(
                name=':desktop: Informazioni Server',
                value=f":beginner: Entrato il {member.joined_at.strftime('%d %b %Y %H:%M')}\n:x: Non boostando il server",
                inline=False
            )
        else:
            embed.add_field(
                name=':desktop: Informazioni Server',
                value=f":beginner: Entrato il {member.joined_at.strftime('%d %b %Y %H:%M')}\n:sparkles: Boostando il server",
                inline=False
            )
        role_str = ''
        for role in member.roles:
            role_str += str(role)+' | '
        embed.add_field(
            name=':busts_in_silhouette: Ruoli',
            value=role_str,
            inline=False
        )
        embed.set_footer(
            text=f'ID: {member.id}'
        )
        await ctx.send(embed=embed)
        
    @commands.command(name='serverinfo', description='Fornirà informazioni sul server.')
    async def serverinfo(self, ctx):
        embed = discord.Embed(
            color=discord.Color.orange(),
            timestamp=ctx.message.created_at
        )
        embed.set_footer(
            text=f'ID: {ctx.guild.id}'
        )
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_author(name=ctx.guild.name)
        embed.add_field(
            name=':desktop: Server info',
            value=f":beginner: Creato il {ctx.guild.created_at.strftime('%d %b %Y %H:%M')}\n:sparkles: Livello boost server: {ctx.guild.premium_tier}\n:globe_with_meridians: Regione Server: {ctx.guild.region}\n:crown: Creatore Server: {ctx.guild.owner.display_name}",
            inline=False
        )
        embed.add_field(
            name=':bust_in_silhouette: Membri',
            value=f"{ctx.guild.member_count} memberi nel server\n{ctx.guild.premium_subscription_count} persone hanno boostato il server",
            inline=False
        )
        role_output = ''
        for role in ctx.guild.roles:
            role_output += str(role)+' | '
        embed.add_field(
            name=':busts_in_silhouette: Ruoli',
            value=role_output,
            inline=False
        )
        await ctx.send(
            embed=embed
        )        
            
    @commands.command(
        name='listserver',
        description='Lista dei server in cui il bot è presente',
        usage='`£listserver`',
        aliases=['ls', 'serverlist', 'sl']        
    )
    async def listserver(self, ctx, page: int = 1):
        output = ''
        guilds = self.bot.guilds
        pages = math.ceil(len(guilds)/10)
        if 1 <= page <= pages:
            counter = 1+(page-1)*10
            for guild in guilds[(page-1)*10:page*10]:
                output += f'{counter}. {guild.name}\n'
                counter += 1
            embed = discord.Embed(
                color=discord.Color.orange(),
                description=output,
                title='**LISTA SERVER**',
                timestamp=ctx.message.created_at
            )
            embed.set_footer(
                text=f'Pagina {page} su {pages}'
            )
            await ctx.send(
                embed=embed
            )
        else:
            await ctx.send(
                embed=create_embed(
                    ':x: La pagina che hai specificato non esiste'
                ),
                delete_after=10
            )            
            
def setup(bot):
    bot.add_cog(Moderation(bot))
