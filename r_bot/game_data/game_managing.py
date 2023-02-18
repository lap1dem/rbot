from .dbinit import data_conn

@data_conn
def create_game(conn, cur, server, thread_id, players_ids, ranked=False):
    if len(players_ids) > 8:
        raise RuntimeError(f"Maximum 8 players allowed, but players_ids has {len(players_ids)}.")
    players = ", ".join(map(str, players_ids))
    cur.execute(f"""
    insert into "gamelist_{server}" values 
    (
    default,
    {thread_id},
    {players},
    default
    )
    """)
    if ranked:
        cur.execute(f"""
                update "gamelist_{server}" set ranked=true where thread_id={thread_id}
            """)
    conn.commit()
    cur.execute(f"""
    select game_id from "gamelist_{server}" where thread_id={thread_id}
    """)
    res = cur.fetchall()
    if len(res) != 0:
        return res[0][0]
    return None
