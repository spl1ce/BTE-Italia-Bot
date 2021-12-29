from discord import Embed, Color
from discord.ext import commands

from os import environ
from utils.spreadsheet import Spreadsheet
from asyncio import sleep

sh = Spreadsheet(environ.get('SPREADSHEET_ID'))


async def refresh_spreadsheet():
    while True:
        sh.fetch()
        await sleep(3600)  # 1 hour


class Approva(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='approva')
    @commands.has_role(704338128692838533)
    async def approva(self, ctx, member=None):
        approva_channel = ctx.guild.get_channel(891675282992431154)
        starter_role = ctx.guild.get_role(704332197628477450)
        newbie_role = ctx.guild.get_role(884464061851521065)
        technical_role = ctx.guild.get_role(696409124102996068)

        if ctx.channel != approva_channel:
            ctx.message.delete()
            return

        if member == None:
            embed = Embed(
                description='Devi indicare un Utente!', color=Color.red())
            ctx.send(embed=embed)
            return

        try:
            converter = commands.MemberConverter()
            member = await converter.convert(ctx, member)
        except commands.MemberNotFound:
            embed = Embed(
                description='Utente non trovato!', color=Color.red())
            await ctx.send(embed=embed)
            return

        if starter_role in member.roles:
            embed = Embed(
                description=f"Utente ha già il ruolo {starter_role.mention}.", color=Color.red())
            await ctx.send(embed=embed)
            return

        try:
            await member.remove_roles(newbie_role)
        except Exception as e:
            print(e)
            embed = Embed(
                description=f"Non è stato possibile rimuovere il ruolo {newbie_role.mention} dal utente.", color=Color.red())
            await ctx.send(embed=embed)
            return

        try:
            await member.add_roles(starter_role)
        except Exception as e:
            print(e)
            embed = Embed(
                description=f"Rimosso il ruolo {newbie_role.mention} ma non è stato possibile assegnare {starter_role.mention}.", color=Color.red())
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
            embed = Embed(
                description=f"{member.name}#{member.discriminator} è stato approvato su Discord ma non su Minecraft, per favore contatta il {technical_role.mention}.", color=Color.gold())
            await ctx.send(embed=embed)
        else:
            # Send lp command to the console channel
            console_channel = ctx.guild.get_channel(
                778281056284442664)

            await console_channel.send(f"lp user {minecraftName} group add starter")

            embed = Embed(
                description=f"Approvato {member.name}#{member.discriminator}!", color=Color.green())
            await ctx.send(embed=embed)

    @approva.error
    async def handler(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            embed = Embed(
                description="Non hai il permesso di usare questo comando.", color=Color.red())
            await ctx.send(embed=embed)
        else:
            print(error)


def setup(bot):
    bot.add_cog(Approva(bot))
    bot.loop.create_task(refresh_spreadsheet())
