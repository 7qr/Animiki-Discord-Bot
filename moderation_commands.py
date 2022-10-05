import datetime
import discord
from discord.ext import commands
from token_bot import __bot_token__

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)


# Displays the Bot username
@bot.event
async def on_ready():
    print(f"{bot.user} has logged in.")


# We start with moderation commands
@bot.command()
@commands.has_permissions(ban_members=True)  # --- > This checks if who calls the command has ban rights
async def ban(ctx, member: discord.Member, *, reason="unspecified reason"):
    if member.id == ctx.author.id:  # --- > This checks if someone it's trying to ban themselves.
        await ctx.send("You can't ban yourself, sorry! ;)")
        return
    else:
        await member.ban(reason=reason)  # ---> In case everything it's good, we ban the member.
        # Ban embed
        embed = discord.Embed(title=f"{ctx.author.name} banned {member.name}", description=f"reason: {reason}",
                              color=0xff0000)
        embed.set_author(name="An user has been banned!", icon_url=ctx.author.display_avatar)
        embed.set_thumbnail(url="https://media.tenor.com/9zCgefg___cAAAAC/bane-no.gif")
        await ctx.send(embed=embed)


@ban.error
async def ban_error(ctx, error):  # -----> This function handles ban errors.
    if isinstance(error, commands.MissingPermissions):  # -- > If someone doesn't have ban rights, raises an error.
        await ctx.send("You have no rights to do that.")
    elif isinstance(error, commands.MissingRequiredArgument):  # ---> If there's a missing argument raises this error.
        await ctx.send("Missing required Argument! If you want to have a look to the usage, please use $help")
    else:
        # In case some unexpected error raises.
        await ctx.send(f"Please contact creator due to the following error: {error}")


@bot.command()
@commands.has_permissions(moderate_members=True)   # ----> This checks if who calls the command has mod rights.
async def mute(ctx, member: discord.Member, time, *, reason=None):
    if member.id == ctx.author.id:  # --- > This checks if someone it's trying to mute themselves.
        await ctx.send("You can't mute yourself, sorry! ;)")
        return
    else:
        # If everything it's fine we step forward and mute the user
        await member.timeout(datetime.timedelta(seconds=int(time)), reason=reason)
        # Mute Embed
        embed = discord.Embed(title=f"{ctx.author.name} muted {member.name}", description=f"reason: {reason}",
                              color=0xff0000)
        embed.set_author(name="An user has been muted!",
                         icon_url=ctx.author.display_avatar)
        embed.set_thumbnail(
            url="https://media4.giphy.com/media/A9FvmJdp3F8hNZK9Ra/giphy.gif?cid="
                "ecf05e47nzhqr89rbj29f15nxmmqrw1pqamip2z6hoa9crex&rid=giphy.gif&ct=g")
        await ctx.send(embed=embed)


@mute.error
async def mute_error(ctx, error):  # ---> This function handles mute_errors
    if isinstance(error, commands.MissingPermissions):  # --> If someone doesn't have mod rights, raises an error.
        await ctx.send("You don't have rights to do that")
    elif isinstance(error, commands.MissingRequiredArgument):  # ---> If there's a missing argument raises this error.
        await ctx.send("Missing required Argument! If you want to have a look to the usage, please use $help")
    else:
        # In case some unexpected error raises.
        await ctx.send(f"Please contact creator due to the following error: {error}")


@bot.command()
@commands.has_permissions(moderate_members=True)   # --- > This checks if who calls the command has mod rights
async def remove_mute(ctx, member: discord.Member, *, reason=None):
    await member.timeout(None)  # --> This removes timeout
    # Unmute Embed
    embed = discord.Embed(title=f"{ctx.author.name} unmuted {member.name}", description=f"reason: {reason}",
                          color=0xff0000)
    embed.set_author(name="An user has been unmuted!",
                     icon_url=ctx.author.display_avatar)
    embed.set_thumbnail(
        url="https://media.tenor.com/SgQCLL1jAL4AAAAC/im-unmuted-im-muted.gif")
    await ctx.send(embed=embed)


@remove_mute.error
async def remove_mute_error(ctx, error):  # ---> This function handles remove_mute_errors
    if isinstance(error, commands.MissingPermissions):  # --> If someone doesn't have mod rights, raises an error.
        await ctx.send("You don't have rights to do that")
    elif isinstance(error, commands.MissingRequiredArgument):   # ---> If there's a missing argument raises this error.
        await ctx.send("Missing required Argument! If you want to have a look to the usage, please use $help")
    else:
        # In case some unexpected error raises.
        await ctx.send(f"Please contact creator due to the following error: {error}")


@bot.command()
@commands.has_permissions(manage_messages=True, read_message_history=True)  # --> This checks if who calls it has rights
async def purge(ctx, channel: discord.TextChannel):
    deleted = await channel.purge(limit=100)  # --> Deletes ALL MESSAGES FROM THE CHANNEL limited to 100.
    await channel.send(f"Deleted {len(deleted)} message(s)")
    # Unmute Embed
    embed = discord.Embed(title=f"{ctx.author.name} DELETED ALL MESSAGES from {channel.name}",
                          color=0xff0000)
    embed.set_author(name="Deleted all messages",
                     icon_url=ctx.author.display_avatar)
    embed.set_thumbnail(
        url="https://media0.giphy.com/media/26ybwwiZmci3DJdYs/giphy.gif?cid=ecf05e47kl6huzkkru6epc5pgo7mwt8bobqactii2w"
            "lg746q&rid=giphy.gif&ct=g")
    await ctx.send(embed=embed)


@purge.error
async def purge_error(ctx, error):  # ---> This function handles purge_errors
    if isinstance(error, commands.MissingPermissions):  # --> If someone doesn't have rights, raises an error.
        await ctx.send("You don't have rights to do that")
    elif isinstance(error, commands.MissingRequiredArgument):  # ---> If there's a missing argument raises this error.
        await ctx.send("Missing required Argument! If you want to have a look to the usage, please use $help")
    else:
        # In case some unexpected error raises.
        await ctx.send(f"Please contact creator due to the following error: {error}")


@bot.command()
@commands.has_permissions(manage_messages=True, read_message_history=True)  # --> This checks if who calls it has rights
async def purge_user(ctx, limit: int, member: discord.Member, reason=None):
    msg = []  # --> We create a list to storage the messages
    async for message in ctx.channel.history():  # ---> For each message in the channel history
        if len(msg) == limit:  # ---> If messages are equal to the limits, the loop ends.
            break
        if message.author == member:  # ---> If the message author is a member, adds those messages to our list
            msg.append(message)
    # Delete all messages from that specific user, that we previously added to our list.
    await ctx.channel.delete_messages(msg)
    # Purge User Embed
    embed = discord.Embed(title=f"{ctx.author.name} deleted {len(msg)} message(s) from {member.name}",
                          description=f"reason: {reason}",
                          color=0xff0000)
    embed.set_author(name="Deleted message(s) from an user",
                     icon_url=ctx.author.display_avatar)
    embed.set_thumbnail(
        url="https://i.gifer.com/7L6q.gif")
    await ctx.send(embed=embed)


@purge_user.error
async def purge_user_error(ctx, error):   # ---> This function handles purge_user_errors
    if isinstance(error, commands.MissingPermissions):  # --> If someone doesn't have rights, raises an error.
        await ctx.send("You don't have rights to do that")
    elif isinstance(error, commands.MissingRequiredArgument):  # ---> If there's a missing argument raises this error.
        await ctx.send("Missing required Argument! If you want to have a look to the usage, please use $help")
    elif isinstance(error, discord.errors.HTTPException):
        # Due to API limitations we can only delete messages under 14 days old.
        await ctx.send("Due to API limits you can only delete messages that are under 14 days old.")
    else:
        # In case some unexpected error raises.
        await ctx.send(f"Please contact creator due to the following error: {error}")


@bot.command()
@commands.has_permissions(kick_members=True)  # --> This checks if who calls it has kicking rights
async def kick(ctx, member: discord.Member, reason=None):
    if member.id == ctx.author.id:  # --> This checks if someone is trying to kick themselves
        await ctx.send("You can't kick yourself, sorry! ;)")
        return
    else:
        await member.kick(reason=reason)  # ---> If everything is perfect, we kick the member.
        # Kick Embed
        embed = discord.Embed(title=f"{ctx.author.name} kicked {member.name}", description=f"reason: {reason}",
                              color=0xff0000)
        embed.set_author(name="Kicked an user!",
                         icon_url=ctx.author.display_avatar)
        embed.set_thumbnail(
            url="https://media0.giphy.com/media/l3V0j3ytFyGHqiV7W/giphy.gif?cid=ecf05e47tslujwgcp5htz0sjwg3cbj5nfnbp27"
                "3e2y4zr5bs&rid=giphy.gif&ct=g")
        await ctx.send(embed=embed)


@kick.error
async def kick_error(ctx, error):  # ---> This function handles kick_error
    if isinstance(error, commands.MissingPermissions):  # --> If someone doesn't have kick rights, raises an error.
        await ctx.send("You don't have rights to do that")
    elif isinstance(error, commands.MissingRequiredArgument):  # ---> If there's a missing argument raises this error.
        await ctx.send("Missing required Argument! If you want to have a look to the usage, please use $help")
    else:
        # In case some unexpected error raises.
        await ctx.send(f"Please contact creator due to the following error: {error}")


bot.run(__bot_token__)  # ---> We run our Bot with our Token from the Discord Dev Portal.
