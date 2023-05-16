from typing import List

import discord as dc
from discord import ButtonStyle

from .CivBanButton import CivBanButton
from ..other_data.emoji_dict import emoji_dict

ALL_NATIONS = list(emoji_dict.keys())


class CivBanView1(dc.ui.View):
    def __init__(self, bans: List[str]):
        super().__init__(timeout=None)
        for i in range(25):
            disabled = True if ALL_NATIONS[i] in bans else False
            style = ButtonStyle.red if ALL_NATIONS[i] in bans else ButtonStyle.secondary
            label = ALL_NATIONS[i][:3]
            button = CivBanButton(label=label, custom_id=ALL_NATIONS[i], emoji=emoji_dict[ALL_NATIONS[i]],
                                  disabled=disabled, style=style)
            self.add_item(button, )


class CivBanView2(dc.ui.View):
    def __init__(self, bans: List[str]):
        super().__init__(timeout=None)
        for i in range(25, 43):
            disabled = True if ALL_NATIONS[i] in bans else False
            style = ButtonStyle.red if ALL_NATIONS[i] in bans else ButtonStyle.secondary
            label = ALL_NATIONS[i][:3]
            button = CivBanButton(label=label, custom_id=ALL_NATIONS[i], emoji=emoji_dict[ALL_NATIONS[i]],
                                  disabled=disabled, style=style)
            self.add_item(button)
