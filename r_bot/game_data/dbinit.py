import os

import psycopg2 as psql
import redis

from .dbinit_secret import redis_url

RCONN = redis.from_url(os.environ.get("REDIS_URL"))
DATABASE_URL = os.environ['DATABASE_URL']
RCONN = redis.Redis(host=redis_url.hostname, port=redis_url.port, password=redis_url.password, ssl=True,
                    ssl_cert_reqs=None)


def data_conn(f):
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = psql.connect(DATABASE_URL, sslmode='require')
            cur = conn.cursor()
            return_val = f(conn, cur, *args, **kwargs)
            return return_val
        except Exception as e:
            print(e)
        finally:
            if conn:
                conn.close()

    return wrapper
