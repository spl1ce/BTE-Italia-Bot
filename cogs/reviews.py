import discord
from discord.ext import commands
from discord.ext.commands import MemberConverter
from discord.ext.commands import PartialEmojiConverter
from discord.ext.commands.errors import MemberNotFound

class Reviews(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        # check if the message is in the reviews channel
        if payload.channel_id == 867045228543606854:
            guild = self.bot.get_guild(payload.guild_id)
            channel = guild.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            ctx = await self.bot.get_context(message)
            emoji_converter = PartialEmojiConverter()
            verify_emoji = await emoji_converter.convert(ctx, '<:Verified:707278127449112616>')

            # check if the message was sent by the bot
            if payload.emoji == verify_emoji:
            
                username = message.embeds[0].fields[0].value
                ign = message.embeds[0].fields[1].value
                macroregion = message.embeds[0].fields[4].value
                city = str(message.embeds[0].fields[5].value).title()
                revisore_role = guild.get_role(830888232609906698)
                log_channel = guild.get_channel(697438179975888966)
                
                try:
                    converter = MemberConverter()
                    member = await converter.convert(ctx, username)
                except commands.MemberNotFound:
                    embed=discord.Embed(description="Member not found.", color=discord.Color.red())
                    await log_channel.send(content=revisore_role.mention, embed=embed)
                    return

                # check if user is in the discord server
                if guild in member.mutual_guilds and len(member.roles) != 1:
                    italiano_role = guild.get_role(698617888675856514)
                    international_role = guild.get_role(698566163738656909)
                    notifiche_channel = guild.get_channel(697169688005836810)
                    console_channel = guild.get_channel(778281056284442664)
                    starter_role = guild.get_role(704332197628477450)
                    nord_role = guild.get_role(698642644640858234)
                    centro_role = guild.get_role(698642874455163052)
                    sud_role = guild.get_role(698642975454003281)

                    # check if member has international role or italiano role
                    if italiano_role in member.roles:
                        notification_message = f'Congratulazioni, {member.mention}!\nSei stato accettato come Starter a {city}.'

                    elif international_role in member.roles:
                        notification_message = f"Congratulations, {member.mention}!\nYou've been accepted as a Starter in {city}"

                    else:
                        embed=discord.Embed(description="Member doesn't have international role nor italiano role.", color=discord.Color.red())
                        await log_channel.send(content=revisore_role.mention, embed=embed)
                        return

                    if macroregion == 'NORD':

                        # send a notification
                        await notifiche_channel.send(notification_message)

                        # gives starter role and macroregion role
                        await member.add_roles(starter_role)
                        await member.add_roles(nord_role)

                        # edits user nickname
                        await member.edit(nick=f'{member.name} [{city}]')

                        # run command in #console
                        await console_channel.send(f'lp user {ign} group add starter')


                    elif macroregion == 'CENTRO':
                        # send a notification
                        await notifiche_channel.send(notification_message)

                        # gives starter role and macroregion role
                        await member.add_roles(starter_role)
                        await member.add_roles(centro_role)

                        # edits user nickname
                        await member.edit(nick=f'{member.name} [{city}]')

                        # run command in #console
                        await console_channel.send(f'lp user {ign} group add starter')


                    elif macroregion == 'SUD':
                        # send a notification
                        await notifiche_channel.send(notification_message)

                        # gives starter role and macroregion role
                        await member.add_roles(starter_role)
                        await member.add_roles(sud_role)

                        # edits user nickname
                        await member.edit(nick=f'{member.name} [{city}]')

                        # run command in #console
                        await console_channel.send(f'lp user {ign} group add starter')

                    else:
                        embed=discord.Embed(description='Macroregion not found.', color=discord.Color.red())
                        await log_channel.send(content=revisore_role.mention, embed=embed)

                else:
                    embed=discord.Embed(description="Member is not in the server or has no roles.", color=discord.Color.red())
                    await log_channel.send(content=revisore_role.mention, embed=embed)
            
            elif payload.emoji == '❌':
                
                username = message.embeds[0].fields[0].value
                notifiche_channel = guild.get_channel(697169688005836810)
                log_channel = guild.get_channel(697438179975888966)
                supporto_channel = guild.get_channel(697382012918562816)
                revisore_role = guild.get_role(830888232609906698)
                italiano_role = guild.get_role(698617888675856514)
                international_role = guild.get_role(698566163738656909)

                try:
                    converter = MemberConverter()
                    member = await converter.convert(ctx, username)
                
                except commands.MemberNotFound:
                    embed=discord.Embed(description="Member not found.", color=discord.Color.red())
                    await log_channel.send(content=revisore_role.mention, embed=embed)
                    return


                if italiano_role in member.roles:    
                    message=f'Ci dispiace {member.mention}!\La tua applicazione è stata rigettata, chiedi in {supporto_channel.mention} la motivazione.'
                    await notifiche_channel.send(message)

                elif international_role in member.roles:
                    message=f"Sorry, {member.mention}!\Your application has been denied, ask in {supporto_channel.mention} the reason."
                    await notifiche_channel.send(message)
                
                else:
                    embed=discord.Embed(description="Member has no roles.", color=discord.Color.red())
                    await log_channel.send(content=revisore_role.mention, embed=embed)


def setup(bot):
    bot.add_cog(Reviews(bot))
    