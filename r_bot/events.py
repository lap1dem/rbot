from .bot import bot
from . import game_data as data
from .management.unlock_server import GameRoles, setup_server_unlock


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await setup_server_unlock()
    bot.add_view(GameRoles())
    for guild in bot.guilds:
        # if guild.id != 980606597581660230 and guild != 1055210867517562940:
        #     await guild.leave()
        #     continue
        if not data.table_exists(f"{guild.name}"):
            data.create_gamelist(guild.name)


@bot.event
async def on_server_join(ctx):
    data.create_gamelist(ctx.guild.name)
