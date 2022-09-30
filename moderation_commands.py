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
        await ctx.send(f"{member.name} has been banned! reason: {reason}")
        # Add ban embed here

@ban.error
async def ban_error(ctx, error):  # -----> This function handles ban errors.
    if isinstance(error, commands.MissingPermissions):  # -- > If someone doesn't have ban rights, raises an error.
        await ctx.send("You have no rights to do that.")



@bot.command()
@commands.has_permissions(administrator=True)
async def unban():
    pass


bot.run(__bot_token__)