import discord as dc
import re
import io
from PIL import Image
import requests

from ..bot import bot
from ..game_data import RCONN
from ..civ5draft import Draft, DraftImage


def split_players(ctx: dc.ApplicationContext, players: str):
    ids = [int(match.group(0)) for match in re.finditer('[0-9]{18,20}', players)]
    return [ctx.guild.get_member(id_) for id_ in ids]


def get_game_dict(tid: int):
    return dict((k.decode('utf8'), v.decode('utf8')) for k, v in RCONN.hgetall(tid).items())


async def send_draft_image(tid):
    thread = await bot.fetch_channel(tid)
    guild = thread.parent.guild
    draft_msg = await thread.send(content="⏳ Generating draft image. Please wait...")
    game_dict = get_game_dict(tid)
    pids = [v for k, v in game_dict.items() if 'player_' in k]
    avatars = {}
    for pid in pids:
        user = await bot.fetch_user(pid)
        if user.avatar is None:
            avatars[game_dict[f"{pid}:name"]] = None
        else:
            av_response = requests.get(user.avatar.url)
            avatars[game_dict[f"{pid}:name"]] = Image.open(io.BytesIO(av_response.content))

    game_dict = get_game_dict(tid)
    bans = [v for k, v in game_dict.items() if ':ban' in k] + game_dict['init_bans'].split(":")
    names = [v for k, v in game_dict.items() if 'name' in k]
    draft = Draft(names, int(game_dict['num_nations']), bans)
    draftimg = DraftImage(draft.drafted_nations, avatars)

    with io.BytesIO() as image_binary:
        draftimg.get_image().save(image_binary, 'PNG')
        image_binary.seek(0)
        await draft_msg.edit(content="", file=dc.File(fp=image_binary, filename='draft_image.png'))
