import random
from typing import Dict, List, Iterable
import os
from PIL import Image
from .image_utils import concat_images, draw_name, draw_avatar
from .config import *


class DraftImage:
    def __init__(self, drafted_nations: Dict[str, List[str]], avatars: Dict[str, Image.Image] = None):
        self.drafted_nations = drafted_nations
        self.avatars = avatars
        self.shuffled_players = list(self.drafted_nations.keys())
        random.shuffle(self.shuffled_players)

        self.draft_blocks = {p_: None for p_ in self.shuffled_players}
        self.draft_names = {p_: None for p_ in self.shuffled_players}

        self._generate_draft_blocks()
        self._generate_draft_names()
        if self.avatars is not None:
            self._draw_avatars()

    def _generate_draft_blocks(self):
        for p_ in self.shuffled_players:
            nations_images = [Image.open(os.path.join(ICONS_CIV_DIR, nation_+".jpg"))
                              for nation_ in self.drafted_nations[p_]]
            self.draft_blocks[p_] = concat_images(nations_images, axis=0)

    def _generate_draft_names(self):
        if self.avatars is None:
            nickpos = 'center'
            namepicfile = 'NAME.jpg'
        else:
            nickpos = 'right'
            namepicfile = 'NAME_AV.jpg'
        namepic = Image.open(os.path.join(ICONS_DIR, namepicfile))
        for i in range(len(self.shuffled_players)):
            p_ = self.shuffled_players[i]
            self.draft_names[p_] = draw_name(self.shuffled_players[i], namepic.copy(), nickpos, slot=i+1)

    def _draw_avatars(self):
        border = Image.open(os.path.join(ICONS_DIR, f"avatars/border.png"))
        for p_ in self.shuffled_players:
            avatar = self.avatars[p_]
            circle = True
            if avatar is None:
                avsum = sum([ord(ch_) for ch_ in p_])
                avatar = Image.open(os.path.join(ICONS_DIR, f"avatars/placeholders/{avsum % 2 + 1}.png"))
                circle = False
            self.draft_names[p_] = draw_avatar(self.draft_names[p_], avatar, circle=circle, border=border)

    def get_image(self):
        blocks = [concat_images([self.draft_names[p_], self.draft_blocks[p_]]) for p_ in self.shuffled_players]
        if (len(blocks) % 2 == 1 and len(blocks) > 3) or len(blocks) < 3:
            return concat_images(blocks, axis=1)
        else:
            row1 = concat_images(blocks[:len(blocks)//2], axis=1)
            row2 = concat_images(blocks[len(blocks)//2:], axis=1)
            return concat_images([row1, row2])

