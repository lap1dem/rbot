import os

from PIL import ImageFont

FILEPATH = os.path.dirname(os.path.abspath(__file__))
ICONS_CIV_DIR = os.path.join(FILEPATH, "icons/icons_civ/")
ICONS_DIR = os.path.join(FILEPATH, "icons/")
FONT_DIR = os.path.join(FILEPATH, "fonts/")

FONT = ImageFont.truetype(os.path.join(FONT_DIR, 'albertus-nova/Albertus Nova.otf'), 92)
SCRIPT_FONT = ImageFont.truetype(os.path.join(FONT_DIR, 'albertus-nova/Albertus Nova Light.otf'), 48)
TINY_FONT = ImageFont.truetype(os.path.join(FONT_DIR, 'albertus-nova/Albertus Nova Light.otf'), 40)
MICRO_FONT = ImageFont.truetype(os.path.join(FONT_DIR, 'albertus-nova/Albertus Nova Light.otf'), 30)

FONT_COLOR = 'black'
