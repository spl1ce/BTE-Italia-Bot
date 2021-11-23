import sqlite3

import discord
from discord.ext import commands


class Reviews(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    async def error(self, error, message_id, discord_name, minecraft_name, macroregion, place):
        conn = sqlite3.connect('./db/db.db')
        cursor = conn.cursor()

        


    async def review(self, payload):
        # check if the message is in the reviews channel
        if payload.channel_id == 867045228543606854:
            guild = self.bot.get_guild(payload.guild_id)
            channel = guild.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            ctx = await self.bot.get_context(message)
            emoji_converter = commands.PartialEmojiConverter()
            verify_emoji = await emoji_converter.convert(ctx, '<:Verified:707278127449112616>')

            # Gets the reactor user and check if it has the role revisore
            reactor = guild.get_member(payload.user_id)
            revisore_role = guild.get_role(830888232609906698)
            log_channel = guild.get_channel(697438179975888966)

            # If the user has not the role revisore, the reaction is removed
            if not revisore_role in reactor.roles:
                embed = discord.Embed(
                    description="<@%d> ha provato ad accettare un membro senza permesso" % (
                        payload.user_id),
                    color=discord.Color.red()
                )
                await log_channel.send(content=revisore_role.mention, embed=embed)
                await message.remove_reaction(verify_emoji, reactor)
                return

            # check if the message was sent by the bot
            if payload.emoji == verify_emoji:
                
                username = message.embeds[0].fields[0].value
                ign = message.embeds[0].fields[1].value
                macroregion = message.embeds[0].fields[4].value
                city = str(message.embeds[0].fields[5].value).title()

                revisore_role = guild.get_role(830888232609906698)
                log_channel = guild.get_channel(697438179975888966)

                try:
                    converter = commands.MemberConverter()
                    member = await converter.convert(ctx, username)
                except commands.MemberNotFound:
                    embed = discord.Embed(
                        description="Member not found.", color=discord.Color.red())
                    await log_channel.send(content=revisore_role.mention, embed=embed)
                    await self.error(error='member_not_found', message_id=payload.message_id, discord_name=username, minecraft_name=ign, macroregion=macroregion, place=city)
                    return

                # check if user is in the discord server
                if guild in member.mutual_guilds and len(member.roles) != 1:
                    italiano_role = guild.get_role(698617888675856514)
                    international_role = guild.get_role(698566163738656909)
                    notifiche_channel = guild.get_channel(697169688005836810)
                    console_channel = guild.get_channel(778281056284442664)
                    newbie_role = guild.get_role(884464061851521065)
                    nord_role = guild.get_role(698642644640858234)
                    centro_role = guild.get_role(698642874455163052)
                    sud_role = guild.get_role(698642975454003281)

                    # check if member has international role or italiano role
                    if italiano_role in member.roles:
                        notification_message = f"Congratulazioni, {member.mention}!\nSei stato accettato come Newbie a {city}."

                    elif international_role in member.roles:
                        notification_message = f"Congratulations, {member.mention}!\nYou've been accepted as a Newbie in {city}"

                    else:
                        embed=discord.Embed(description="Member doesn't have international role nor italiano role.", color=discord.Color.red())
                        await log_channel.send(content=revisore_role.mention, embed=embed)
                        return

                    # send a notification
                    await notifiche_channel.send(notification_message)

                    # gives starter role and macroregion role
                    await member.add_roles(newbie_role)

                    # edits user nickname
                    await member.edit(nick=f'{member.name} [{city}]')

                    # run command in #console
                    await console_channel.send(f'lp user {ign} group add Newbie')

                    if macroregion == 'NORD':
                        await member.add_roles(nord_role)
                    elif macroregion == 'CENTRO':
                        await member.add_roles(centro_role)
                    elif macroregion == 'SUD':
                        await member.add_roles(sud_role)

                    # ERROR macroregion not found
                    else:
                        embed = discord.Embed(
                            description='Macroregion not found.', color=discord.Color.red())
                        await log_channel.send(content=revisore_role.mention, embed=embed)
                        await self.error(error='macroregion_not_found', message_id=payload.message_id, discord_name=username, minecraft_name=ign, macroregion=macroregion, place=city)
                else:
                    embed = discord.Embed(
                        description="Member is not in the server or has no roles.", color=discord.Color.red())
                    await log_channel.send(content=revisore_role.mention, embed=embed)

            elif payload.emoji == '❌':

                username = message.embeds[0].fields[0].value
                ign = message.embeds[0].fields[1].value
                macroregion = message.embeds[0].fields[4].value
                city = str(message.embeds[0].fields[5].value).title()

                username = message.embeds[0].fields[0].value
                notifiche_channel = guild.get_channel(697169688005836810)
                log_channel = guild.get_channel(697438179975888966)
                supporto_channel = guild.get_channel(697382012918562816)
                revisore_role = guild.get_role(830888232609906698)
                italiano_role = guild.get_role(698617888675856514)
                international_role = guild.get_role(698566163738656909)

                try:
                    converter = commands.MemberConverter()
                    member = await converter.convert(ctx, username)

                except commands.MemberNotFound:
                    embed = discord.Embed(
                        description="Member not found.", color=discord.Color.red())
                    await log_channel.send(content=revisore_role.mention, embed=embed)
                    await self.error(error='member_not_found', message_id=payload.message_id, discord_name=username, minecraft_name=ign, macroregion=macroregion, place=city)
                    return

                if italiano_role in member.roles:
                    message = f'Ci dispiace {member.mention}!\La tua applicazione è stata rigettata, chiedi in {supporto_channel.mention} la motivazione.'
                    await notifiche_channel.send(message)

                elif international_role in member.roles:
                    message = f"Sorry, {member.mention}!\Your application has been denied, ask in {supporto_channel.mention} the reason."
                    await notifiche_channel.send(message)

                else:
                    embed = discord.Embed(
                        description="Member has no roles.", color=discord.Color.red())
                    await log_channel.send(content=revisore_role.mention, embed=embed)


    # USER REACTION
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id == 867045228543606854:
            guild = self.bot.get_guild(payload.guild_id)
            channel = guild.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            ctx = await self.bot.get_context(message)
            emoji_converter = commands.PartialEmojiConverter()
            verify_emoji = await emoji_converter.convert(ctx, '<:Verified:707278127449112616>')

            # Gets the reactor user and check if it has the role revisore
            reactor = guild.get_member(payload.user_id)
            revisore_role = guild.get_role(830888232609906698)
            log_channel = guild.get_channel(697438179975888966)

            # If the user has not the role revisore, the reaction is removed
            if not revisore_role in reactor.roles:
                embed = discord.Embed(
                    description="<@%d> ha provato ad accettare un membro senza permesso" % (
                        payload.user_id),
                    color=discord.Color.red()
                )
                await log_channel.send(content=revisore_role.mention, embed=embed)
                await message.remove_reaction(verify_emoji, reactor)
                return
            
            await self.review(self,payload=payload)


    # FIX COMMAND
    @commands.command(name='fix')
    async def fix(self, ctx, number, fix, value):
    

def setup(bot):
    bot.add_cog(Reviews(bot))
