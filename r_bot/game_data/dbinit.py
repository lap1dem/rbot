import os
from urllib.parse import urlparse
import redis
import psycopg2 as psql

RCONN = redis.from_url(os.environ.get("REDIS_URL"))
DATABASE_URL = os.environ['DATABASE_URL']
# url = urlparse("redis://:p74b9c7ec1b81e3384a5b6a77076443a17f34c2273316d001165144013def44b5@ec2-52-208-16-24.eu-west-1"
#                ".compute.amazonaws.com:26780")
# RCONN = redis.Redis(host=url.hostname, port=url.port, password=url.password, ssl=True, ssl_cert_reqs=None)
# DATABASE_URL = "postgres://pbhzrbwqdhdasc:308079183f945c73cdd99f3444243ef2c5ff9e2f8543f6f7fcd91a51f1e7cc69@ec2-34-252" \
#                "-35-249.eu-west-1.compute.amazonaws.com:5432/db841kk2il7u68"




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
