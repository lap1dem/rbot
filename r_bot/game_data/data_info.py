from .dbinit import data_conn


@data_conn
def table_exists(conn, cur, guild_name: str):
    query = f"""
       SELECT FROM pg_tables WHERE schemaname='public' AND tablename='gamelist_{guild_name}'
       """
    cur.execute(query)
    res = cur.fetchall()
    if len(res) == 0:
        return False
    return True
