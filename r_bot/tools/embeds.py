import discord as dc

from ..game_data import RCONN


def ban_progress_embed(tid: int):
    num_players = int(RCONN.hget(tid, "num_players"))
    num_bans = int(RCONN.hget(tid, "num_bans"))
    players = RCONN.hmget(tid, [f"player_{i}" for i in range(num_players)])
    players = [p_.decode('utf-8') for p_ in players]
    names = RCONN.hmget(tid, [f"{pid}:name" for pid in players])
    names = [n_.decode("utf-8") for n_ in names]
    pbans = {names[i]: [RCONN.hexists(tid, f"{players[i]}:ban{j}")
                        for j in range(1, num_bans + 1)] for i in range(num_players)}
    embed = dc.Embed(title="Each player must ban two nations", colour=dc.Colour.blue())
    for name in names:
        bans = " ".join(["✅" if be else "⬛" for be in pbans[name]])
        embed.add_field(name=name, value=bans)
    full_bans = all([False not in bans for _, bans in pbans.items()])
    return embed, full_bans
