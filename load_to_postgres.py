import psycopg2
from psycopg2.extras import DictCursor
import configs

pg_connection = psycopg2.connect(**configs.POSTGRES)
pg_cursor = pg_connection.cursor(cursor_factory=DictCursor)
