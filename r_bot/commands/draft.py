import discord as dc
import io

import requests
from PIL import Image

from ..bot import bot
from ..civ5draft import Draft, DraftImage
from ..views.CivBanView import CivBanView1, CivBanView2
from ..tools.utils import split_players
from ..tools.embeds import ban_progress_embed
from ..game_data import RCONN, create_game
from ..localization.draft import *
from ..localization.general import *


@bot.slash_command(
    name=draft_command_name['en-GB'],
    name_localizations=draft_command_name,
    description=draft_command_desc['en-GB'],
    description_localizations=draft_command_desc
)
async def draft(
        ctx: dc.ApplicationContext,
        players: dc.Option(str, name=draft_par_players_name['en-GB'], name_localizations=draft_par_players_name,
                           description=draft_par_players_desc['en-GB'],
                           description_localizations=draft_par_players_desc),
        number: dc.Option(int, name=draft_par_number_name['en-GB'], name_localizations=draft_par_number_name,
                          description=draft_par_number_desc['en-GB'], description_localizations=draft_par_number_desc,
                          required=False, default=3, max_value=6),
        skipbans: dc.Option(int, name=draft_par_skipbans_name['en-GB'], name_localizations=draft_par_skipbans_name,
                            description=draft_par_skipbans_desc['en-GB'],
                            description_localizations=draft_par_skipbans_desc,
                            required=False, choices=[option_choice_yes, option_choice_no], default=option_choice_no),
        stdbans: dc.Option(int, name=draft_par_stdbans_name['en-GB'], name_localizations=draft_par_stdbans_name,
                           description=draft_par_stdbans_desc['en-GB'],
                           description_localizations=draft_par_stdbans_desc,
                           required=False, choices=[option_choice_yes, option_choice_no], default=option_choice_yes),
):
    stdbans = stdbans.value if not isinstance(stdbans, int) else stdbans
    skipbans = skipbans.value if not isinstance(skipbans, int) else skipbans
    init_bans = ['Huns', 'Venice', 'Spain'] if stdbans else []

    players = split_players(ctx, players)
    if len(set(players)) < len(players):
        await ctx.respond(
            draft_unique_error.get(ctx.interaction.locale, draft_unique_error['en-GB']),
            ephemeral=True)
        return

    player_ids = [p.id for p in players]
    player_tags = [f"<@{pid}>" for pid in player_ids]
    skipbans = int(skipbans)
    if skipbans:
        try:
            reaction = await ctx.respond(content=draft_skipbans_wait.get(ctx.guild.preferred_locale, draft_skipbans_wait['en-GB']))
            await draft_without_bans(reaction, player_ids, number, init_bans)
            return
        except Exception as e:
            print(e)
            return
    else:
        if isinstance(ctx.channel, dc.Thread):
            await ctx.respond(
                draft_thread_error.get(ctx.interaction.locale, draft_thread_error['en-GB']),
                ephemeral=True)
            return

    if len(players) > 8:
        await ctx.respond(
            draft_players_num_error.get(ctx.interaction.locale, draft_players_num_error['en-GB']),
            ephemeral=True)
        return

    reaction = await ctx.respond(content=", ".join([f"<@{p.id}>" for p in players]))
    msg_thread = await reaction.original_response()
    thread = await ctx.channel.create_thread(
        name="⏳ Wait a moment",
        message=msg_thread)

    game_id = create_game(ctx.guild.name, thread.id, player_ids)
    thread_name = draft_thread_name.get(ctx.guild.preferred_locale, draft_thread_name['en-GB']) + f" {game_id}"
    await thread.edit(name=thread_name)

    for p in players:
        await thread.add_user(p)
    db_dict = {f"player_{i}": players[i].id for i in range(len(players))}
    db_dict.update({f"{p.id}:name": p.name for p in players})
    db_dict["num_nations"] = number
    db_dict["num_players"] = len(players)
    db_dict["num_bans"] = 2
    db_dict["init_bans"] = ":".join(init_bans)
    RCONN.hset(thread.id, mapping=db_dict)
    ban_embed, _ = ban_progress_embed(thread.id)
    ban_msg = await thread.send(view=CivBanView1(bans=init_bans), embed=ban_embed)
    await ban_msg.edit(embed=ban_embed)
    ban_msg2 = await thread.send(view=CivBanView2(bans=init_bans))
    RCONN.hset(thread.id, "ban_msg_id", ban_msg.id)
    RCONN.hset(thread.id, "ban_msg_id2", ban_msg2.id)


async def draft_without_bans(reaction, pids, num_nations=3, bans=[]):
    avatars = {}
    names = []
    for pid in pids:
        user = await bot.fetch_user(pid)
        names.append(user.name)
        if user.avatar is None:
            avatars[user.name] = None
        else:
            av_response = requests.get(user.avatar.url)
            avatars[user.name] = Image.open(io.BytesIO(av_response.content))

    bans_ = [] + bans
    draft = Draft(names, num_nations, bans_)
    draftimg = DraftImage(draft.drafted_nations, avatars)

    with io.BytesIO() as image_binary:
        draftimg.get_image().save(image_binary, 'PNG')
        image_binary.seek(0)
        await reaction.edit_original_response(content="", file=dc.File(fp=image_binary, filename='draft_image.png'))
