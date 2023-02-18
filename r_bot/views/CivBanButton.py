import discord as dc
from discord import ButtonStyle, Emoji, PartialEmoji, Interaction

from ..game_data import RCONN, create_game
from ..tools.embeds import ban_progress_embed
from ..tools.utils import send_draft_image
from ..localization.draft import *


class CivBanButton(dc.ui.Button):
    def __init__(
            self,
            style: ButtonStyle = ButtonStyle.secondary,
            label: str | None = None,
            disabled: bool = False,
            custom_id: str | None = None,
            url: str | None = None,
            emoji: str | Emoji | PartialEmoji | None = None,
            row: int | None = None,
    ):
        super().__init__(style=style, label=label, disabled=disabled,
                         custom_id=custom_id, url=url, emoji=emoji, row=row)

    async def callback(self, interaction: Interaction):
        tid = interaction.channel_id
        if RCONN.hexists(tid, self.emoji.name):
            await interaction.response.send_message(
                draft_ban_pressed.get(interaction.locale, draft_ban_pressed['en-GB']).format(self.emoji.name),
                ephemeral=True)
            return
        else:
            RCONN.hset(tid, self.emoji.name, 1)

        pid = interaction.user.id
        ban1_exists = RCONN.hexists(tid, f"{pid}:ban1")
        ban2_exists = RCONN.hexists(tid, f"{pid}:ban2")
        if ban1_exists and ban2_exists:
            await interaction.response.send_message(
                draft_ban_limit.get(interaction.locale, draft_ban_limit['en-GB']), ephemeral=True)
            RCONN.hdel(tid, self.emoji.name)
            return
        elif ban1_exists:
            RCONN.hset(tid, f"{pid}:ban2", self.emoji.name)
        else:
            RCONN.hset(tid, f"{pid}:ban1", self.emoji.name)
        self.style = dc.ButtonStyle.red
        self.disabled = True
        await interaction.response.edit_message(view=self.view)
        ban_msg = await interaction.channel.fetch_message(RCONN.hget(tid, "ban_msg_id").decode("utf-8"))
        embed, full_bans = ban_progress_embed(tid)
        await ban_msg.edit(embed=embed)
        if full_bans and not RCONN.hexists(tid, "started"):
            RCONN.hset(tid, "started", 1)
            await send_draft_image(tid)
