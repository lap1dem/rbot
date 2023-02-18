from .dbinit import data_conn


@data_conn
def create_gamelist(conn, cur, server):
    query = f"""
    create table if not exists "gamelist_{server}"
    (
    game_id serial not null primary key,
    thread_id bigint not null default 0,
    player_1 bigint,
    player_2 bigint,
    player_3 bigint,
    player_4 bigint,
    player_5 bigint,
    player_6 bigint,
    player_7 bigint,
    player_8 bigint,
    autobans text,
    bans_1 text,
    bans_2 text,
    bans_3 text,
    bans_4 text,
    bans_5 text,
    bans_6 text,
    bans_7 text,
    bans_8 text,
    draft_1 text,
    draft_2 text,
    draft_3 text,
    draft_4 text,
    draft_5 text,
    draft_6 text,
    pick_1 text,
    pick_2 text,
    pick_3 text,
    pick_4 text,
    pick_5 text,
    pick_6 text,
    dt timestamp,
    canceled boolean not null default false,
    finished boolean not null default false,
    winner bigint,
    ranked boolean not null default false,
    dr_1 float,
    dr_2 float,
    dr_3 float,
    dr_4 float,
    dr_5 float,
    dr_6 float,
    dr_7 float,
    dr_8 float
    )
    """
    cur.execute(query)
    conn.commit()
