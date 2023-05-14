import discord
from ..bot import bot
from .config import GUILD_ID
from . import roles


async def _get_remove_role(interaction, role_id, role_name):
    member = interaction.user
    role = interaction.guild.get_role(role_id)
    if role in member.roles:
        embed = discord.Embed(
            colour=discord.Colour.red(), description=f"Removed role `{role_name}`"
        )
        await member.remove_roles(role)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(
            colour=discord.Colour.green(), description=f"Added role `{role_name}`"
        )
        await member.add_roles(role)
        await interaction.response.send_message(embed=embed, ephemeral=True)

class GameRoles(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Civilization V",
        custom_id="civ5",
        style=discord.ButtonStyle.primary,
        emoji=":_game_civ5:981318724843896832",
    )
    async def civ5_button_callback(self, button, interaction):
        await _get_remove_role(interaction, roles.Civilization_V_ID, 'Civilization V')

    @discord.ui.button(
        label="Humankind",
        custom_id="humankind",
        style=discord.ButtonStyle.primary,
        emoji=":_game_humankind:981318723774337084",
    )
    async def humankind_button_callback(self, button, interaction):
        await _get_remove_role(interaction, roles.Humankind_ID, 'Humankind')

    @discord.ui.button(
        label="Gremlins Inc.",
        custom_id="gremlinsinc",
        style=discord.ButtonStyle.primary,
        emoji=":_game_gremlins:983773789429059605",
    )
    async def gremlinsinc_button_callback(self, button, interaction):
        await _get_remove_role(interaction, roles.Gremlins_Inc_ID, 'Gremlins Inc.')


async def setup_server_unlock():
    guild = bot.get_guild(GUILD_ID)
    channel = guild.get_channel(980607013727928380)
    messages = await channel.history(limit=5).flatten()
    for msg in messages:
        if msg.author.id == bot.user.id:
            return
    await channel.send(
        "**Select categories you want to unlock**\n*Виберіть групи каналів для розблокування*",
        view=GameRoles(),
    )
