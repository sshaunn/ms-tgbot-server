import logging
import psycopg
import src.consts as c

from psycopg.rows import class_row, dict_row


def get_db_connection():
    # postgresql: // user: qpVTacISnsvdOYGHAMKJ3WSzPV2QgG3T @ dpg - cpvi0vpu0jms73at8ps0 - a / erp4btc
    # postgresql://user:qpVTacISnsvdOYGHAMKJ3WSzPV2QgG3T@dpg-cpvi0vpu0jms73at8ps0-a.singapore-postgres.render.com/erp4btc
    print("env=", c.ENV)
    if c.ENV == 'prod':
        return psycopg.connect(f"host={c.DBHOST_PROD} dbname={c.DBNAME_PROD} user={c.DB_USERNAME_PROD} "
                               f"password={c.DB_PASSWORD_PROD}", row_factory=dict_row)
    return psycopg.connect(f"host={c.DBHOST} dbname={c.DBNAME} user={c.DB_USERNAME} password={c.DB_PASSWORD}",
                               row_factory=dict_row)


def exec_cursor(sql_query, *values):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql_query, values)
        conn.commit()
        conn.close()


def fetch_cursor(sql_query, *values):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql_query, values)
            record = cur.fetchone()
            conn.close()
        return record


def fetch_all_cursor(sql_query):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql_query)
            records = cur.fetchall()
            conn.close()
        return records


def fetch_all_cursor_with_conditions(sql_query, *value):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql_query, *value)
            records = cur.fetchall()
            conn.close()
        return records
