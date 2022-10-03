import datetime

import discord
from discord.ext import commands
from token_bot import __bot_token__

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)

# Displays the bot's username


@bot.event
async def on_ready():
    print(f"{bot.user} has logged in.")


@bot.command()
@commands.has_permissions(ban_members=True)  # --- > This checks if who calls the command has ban rights
async def ban(ctx, member: discord.Member, *, reason="unspecified reason"):
    if member.id == ctx.author.id:  # --- > This checks if someone it's trying to ban themself.
        await ctx.send("You can't ban yourself, sorry! ;)")
        return
    else:
        await member.ban(reason=reason)  # ---> In case everything it's good, we ban the member.
        # Ban embed
        embed = discord.Embed(title=f"{ctx.author.name} banned {member.name}", description=f"reason: {reason}",
                              color=0xff0000)
        embed.set_author(name="An user has been banned!")
        embed.set_thumbnail(url="https://media.tenor.com/9zCgefg___cAAAAC/bane-no.gif")
        await ctx.send(embed=embed)


@ban.error
async def ban_error(ctx, error):  # -----> This function handles ban errors.
    if isinstance(error, commands.MissingPermissions):  # -- > If someone doesn't have ban rights, raises an error.
        await ctx.send("You have no rights to do that.")


@bot.command()
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, time, *, reason=None):
    if member.id == ctx.author.id:  # --- > This checks if someone it's trying to mute themself.
        await ctx.send("You can't mute yourself, sorry! ;)")
        return
    else:
        await member.timeout(datetime.timedelta(seconds=int(time)), reason=reason)
        await ctx.send(f"{member.name} has been muted because: {reason}")
        # Add embed here


@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have rights to do that")


@bot.command()
@commands.has_permissions(moderate_members=True)
async def remove_mute(ctx, member: discord.Member, *, reason=None):
    await member.timeout(None)
    await ctx.send(f"{member.name} has been unmuted {reason}")
    # Add embed here


@remove_mute.error
async def remove_mute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have rights to do that")





@bot.command()
@commands.has_permissions(read_message_history=True)
async def purge(ctx, channel: discord.TextChannel, member: discord.Member):
    pass

bot.run(__bot_token__)

