import os
import random
import numpy as np
from typing import Iterable

from PIL import Image, ImageDraw, ImageOps
from .config import *


def concat_images(images: Iterable[Image.Image], axis: int = 0):
    widths = [im.width for im in images]
    heights = [im.height for im in images]

    if axis == 0:
        tot_width = max(widths)
        tot_height = sum(heights)
        res = Image.new('RGB', (tot_width, tot_height))
        cur_height = 0

        for img in images:
            res.paste(img, (0, cur_height))
            cur_height += img.height

    elif axis == 1:
        tot_width = sum(widths)
        tot_height = max(heights)
        res = Image.new('RGB', (tot_width, tot_height))
        cur_width = 0

        for img in images:
            res.paste(img, (cur_width, 0))
            cur_width += img.width
    else:
        raise ValueError("Axis must be set ether to 0 or 1.")
    return res


def draw_name(name: str, namepic: Image.Image, position: str = 'center', slot: int = None):
    namepic = namepic.convert("RGBA")
    draw = ImageDraw.Draw(namepic)
    back_w, back_h = namepic.size
    text_w, text_h = draw.textsize(name, font=FONT)
    if position == 'center':
        text_pos = ((back_w - text_w) / 2, (back_h - text_h) / 2)
    else:
        text_pos = ((back_w - text_w) / 2 + back_w / 8, (back_h - text_h) / 2)

    draw.text(text_pos, name, font=FONT, fill=FONT_COLOR)

    if slot is not None:
        if position == 'center':
            text_w, text_h = draw.textsize(str(slot), font=SCRIPT_FONT)
            text_pos = (30, 20)
            draw.text(text_pos, str(slot), font=SCRIPT_FONT, fill=FONT_COLOR)
            draw.ellipse((text_pos[0] + text_w//2 - 32, text_pos[1] + text_h//2 - 32,
                          text_pos[0] + text_w//2 + 32, text_pos[1] + text_h//2 + 32),
                         fill=None, outline=(0, 0, 0), width=6)
        # draw.ellipse((16, 8, 80, 72), fill=None, outline=(0, 0, 0), width=6)
        else:
            slotname = f"( {slot} )"
            txt = Image.new('RGBA', namepic.size, (255, 255, 255, 0))
            text_w, text_h = draw.textsize(slotname, font=TINY_FONT)
            text_pos = ((back_w - text_w) / 2 - back_w / 4 - 10, 16)
            draw.text(text_pos, slotname, font=TINY_FONT, fill=FONT_COLOR)

    return namepic


def draw_avatar(background: Image.Image, avatar: Image.Image, circle=False,
                border: Image.Image = None, av_side: int = 212):
    av_res = avatar.resize((av_side, av_side)).convert("RGBA")
    background = background.convert("RGBA")

    if circle:
        mask = Image.new('L', av_res.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.pieslice([(0, 0), av_res.size], 0, 360, fill=255)
    else:
        mask = Image.new('L', av_res.size, 255)
    if border is not None:
        border = border.resize((av_side, av_side))
        av_res = Image.alpha_composite(av_res, border)
        # av_res.show()
        # assert 1==0
    foreground = Image.new("RGBA", background.size)
    box_side = (256 - av_side)//2
    foreground.paste(av_res, box=(box_side, box_side), mask=mask)
    res = Image.alpha_composite(background, foreground)

    draw = ImageDraw.Draw(res)
    contour_line_width = 4
    # draw.line([(0, 0), (res.width, 0)], fill="black", width=contour_line_width)
    draw.line([(0, res.height-6), (res.width, res.height-6)], fill="black", width=contour_line_width)

    # if not circle:
    #     pass
        # draw = ImageDraw.Draw(background)
        # draw.rectangle((32, 32, 222, 222), fill=None, outline=(0, 0, 0), width=6)
    return res


def crop_circle(image: Image.Image):
    mask = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.pieslice([(0, 0), image.size], 0, 360, fill=255)
    output = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    return output
