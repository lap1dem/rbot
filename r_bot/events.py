from .bot import bot
from . import game_data as data


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    for guild in bot.guilds:
        if not data.table_exists(f"{guild.name}"):
            data.create_gamelist(guild.name)


@bot.event
async def on_server_join(ctx):
    data.create_gamelist(ctx.guild.name)
