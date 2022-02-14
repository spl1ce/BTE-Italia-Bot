from discord.ext import commands
from discord import Color, Embed


class Reviews(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        # check if the message is in the reviews channel
        if payload.channel_id == 867045228543606854:
            guild = self.bot.get_guild(payload.guild_id)
            channel = guild.get_channel(payload.channel_id)
            console_channel = guild.get_channel(778281056284442664)
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
                embed = Embed(
                    description=f"{revisore_role.mention} ha provato ad accettare un membro senza permesso",
                    color=Color.red()
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

                try:
                    converter = commands.MemberConverter()
                    member = await converter.convert(ctx, username)
                except commands.MemberNotFound:
                    embed = Embed(
                        description="Utente non trovato.", color=Color.red())
                    await log_channel.send(content=revisore_role.mention, embed=embed)
                    return

                # run command in #console
                await console_channel.send(f'lp user {ign} group add Newbie')

                # check if user is in the discord server
                if guild in member.mutual_guilds and len(member.roles) != 1:
                    italiano_role = guild.get_role(698617888675856514)
                    international_role = guild.get_role(698566163738656909)
                    notifiche_channel = guild.get_channel(697169688005836810)
                    newbie_role = guild.get_role(884464061851521065)
                    nord_role = guild.get_role(698642644640858234)
                    centro_role = guild.get_role(698642874455163052)
                    sud_role = guild.get_role(698642975454003281)

                    # check if member has international role or italiano role
                    if italiano_role in member.roles:
                        notification_message = f"Congratulazioni, {member.mention}!\nSei stato accettato come _Newbie_ a _{city}_."

                    elif international_role in member.roles:
                        notification_message = f"Congratulations, {member.mention}!\nYou've been accepted as a _Newbie_ in _{city}_."

                    else:
                        embed = Embed(
                            description=f"L'utente non ha né {italiano_role.mention}, né {international_role.mention}.\nÈ stato comunque approvato su Minecraft.", color=Color.gold())
                        await log_channel.send(content=revisore_role.mention, embed=embed)
                        return

                    # send a notification
                    await notifiche_channel.send(notification_message)

                    # gives starter role and macroregion role
                    await member.add_roles(newbie_role)

                    # edits user nickname
                    await member.edit(nick=f'{member.name} [{city}]')

                    if macroregion == 'NORD':
                        await member.add_roles(nord_role)
                    elif macroregion == 'CENTRO':
                        await member.add_roles(centro_role)
                    elif macroregion == 'SUD':
                        await member.add_roles(sud_role)
                    else:
                        embed = Embed(
                            description="Macroregione errata.\nL'utente è stato comunque approvato su Minecraft.", color=Color.gold())
                        await log_channel.send(content=revisore_role.mention, embed=embed)

                else:
                    embed = Embed(
                        description="L'utente non è nel server.\nÈ stato comunque approvato su Minecraft.", color=Color.gold())
                    await log_channel.send(content=revisore_role.mention, embed=embed)

            elif str(payload.emoji) == '❌':

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
                    embed = Embed(
                        description="Utente non trovato.", color=Color.red())
                    await log_channel.send(content=revisore_role.mention, embed=embed)
                    return

                if italiano_role in member.roles:
                    message = f'Ci dispiace {member.mention}!\nLa tua applicazione è stata rigettata, chiedi in {supporto_channel.mention} la motivazione.'
                    await notifiche_channel.send(message)

                elif international_role in member.roles:
                    message = f"Sorry, {member.mention}!\nYour application has been denied, ask in {supporto_channel.mention} the reason."
                    await notifiche_channel.send(message)

                else:
                    embed = Embed(
                        description="L'utente non ha ruoli", color=Color.red())
                    await log_channel.send(content=revisore_role.mention, embed=embed)

    @commands.command(name='unsafe_accetta_revisione', aliases=['uar'])
    @commands.has_role(942773350080581692)
    async def unsafe_accetta_revisione(self, ctx, member=None, minecraft_name=None):
        if member is None or minecraft_name is None:
            embed = Embed(
                description="Devi specivicare nome utente sia di Discord che di Minecraft.", color=Color.red())
            await ctx.send(embed=embed)
            return

        # Converts the member to a discord.Member object
        try:
            converter = commands.MemberConverter()
            member = await converter.convert(ctx, member)

            # Check if the member is in the discord server
            if member.guild != ctx.guild:
                raise commands.MemberNotFound()
        except commands.MemberNotFound:
            embed = Embed(
                description='Utente non trovato o non è nel server!', color=Color.red())
            await ctx.send(embed=embed)
            return

        italiano_role = ctx.guild.get_role(698617888675856514)
        international_role = ctx.guild.get_role(698566163738656909)
        newbie_role = ctx.guild.get_role(884464061851521065)
        notifiche_channel = ctx.guild.get_channel(697169688005836810)
        console_channel = ctx.guild.get_channel(778281056284442664)

        # run command in #console
        await console_channel.send(f'lp user {minecraft_name} group add Newbie')

        # check if member has international role or italiano role
        if italiano_role in member.roles:
            notification_message = f"Congratulazioni, {member.mention}!\nSei stato accettato come _Newbie_."
        elif international_role in member.roles:
            notification_message = f"Congratulations, {member.mention}!\nYou've been accepted as a _Newbie_."
        else:
            embed = Embed(
                description=f"L'utente non ha né {italiano_role.mention}, né {international_role.mention}.\nÈ stato comunque approvato su Minecraft.", color=Color.gold())
            await ctx.send(embed=embed)
            return

        await notifiche_channel.send(notification_message)

        # gives starter role and macroregion role
        await member.add_roles(newbie_role)


def setup(bot):
    bot.add_cog(Reviews(bot))
