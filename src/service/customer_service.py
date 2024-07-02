from psycopg.errors import UniqueViolation

import src.consts as c
import time
import datetime as dt
from datetime import datetime

from src.bitget import utils
from src.bitget.bitget_api import BitgetApi as baseApi
from src.bitget.utils import epoch_date_formater
from src.config import dbconfig
from src.logger import log
from src.service.customers import Customer


def get_customer_by_client_uid(uid):
    request = baseApi(c.ACCESS_KEY, c.SECRET_KEY, c.PASSPHRASE)
    params = {"uid": uid,
              "pageNo": 1,
              "pageSize": 1000
              }
    response = request.post(c.AGENT_ENDPOINT, params)
    time.sleep(0.1)
    if not response["data"]:
        return None
    return response["data"][0]


def save_customer(uid, firstname, lastname, tgid, register_time, is_member=False, is_whitelist=False, is_ban=False,
                  join_time=None, left_time=None):
    formated_date = epoch_date_formater(register_time)
    try:
        dbconfig.exec_cursor("""
        INSERT INTO erp4btc.customers (uid, firstname, lastname, tgid, register_time, is_member, is_whitelist, is_ban, 
        join_time, left_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                             uid, firstname, lastname, tgid, formated_date, is_member, is_whitelist, is_ban,
                             join_time, left_time)
        customer = Customer(uid, firstname, lastname, tgid, register_time, is_member, is_whitelist, is_ban, join_time,
                            left_time)
        log.info("saving customer record into database, customer=%s", customer.to_dict())
        return customer.to_dict()
    except UniqueViolation as uv:
        log.error("Error occurred when inserting customer record with uid=%s, and exception=%s", uid, uv)
        return None
    except Exception as ex:
        log.error("Error occurred when inserting customer record with uid=%s, and exception=%s", uid, ex)
        return None


def update_customer_membership(uid, membership):
    try:
        dbconfig.exec_cursor("""
        INSERT INTO erp4btc.customers (uid, is_member) 
        VALUES (%s, %s)
        ON CONFLICT (uid) DO UPDATE 
        SET is_member=EXCLUDED.is_member""", uid, membership)
        return {"uid": uid, "is_member": membership, "message": "membership updated success"}
    except Exception as ex:
        log.error("Error occurred when inserting customer record with uid=%s, and exception=%s", uid, ex)
        return None


def update_customer_ban_status(uid, is_member, is_ban, left_time):
    try:
        dbconfig.exec_cursor("""
        INSERT INTO erp4btc.customers (uid, is_member, is_ban, left_time) 
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (uid) DO UPDATE SET 
        is_member=EXCLUDED.is_member,
        is_ban=EXCLUDED.is_ban,
        left_time=EXCLUDED.left_time""", uid, is_member, is_ban, left_time)
        return {"uid": uid,
                "is_member": is_member,
                "is_ban": is_ban,
                "left_time": left_time,
                "message": "user banned success"}
    except Exception as ex:
        log.error("Error occurred when inserting customer record with uid=%s, and exception=%s", uid, ex)
        return None


def get_customer_by_uid(uid):
    try:
        record = dbconfig.fetch_cursor("""
        SELECT * FROM erp4btc.customers 
        WHERE uid=%s""", uid)
        if record:
            log.info("fetching customer by uid=%s, record=%s ", uid, record)
            return record
        else:
            return None
    except Exception as ex:
        log.error("Error occurred when fetching customer record with uid=%s, exception=%s", uid, ex)
        return None


def get_customer_by_key(keyname, value):
    try:
        record = dbconfig.fetch_cursor(
            f"SELECT uid, firstname, lastname, tgid, register_time FROM erp4btc.customers WHERE {keyname}=%s", value)
        if record:
            log.info(f"fetching customer by {keyname}=%s, record=%s", value, record)
            return record
        else:
            return None
    except Exception as ex:
        log.error("Error occurred when fetching customer record with %s=%s, exception=%s", keyname, value, ex)
        return None


def update_customer_rejoin(uid, is_ban):
    try:
        dbconfig.exec_cursor("""
        INSERT INTO erp4btc.customers (uid, is_ban, is_member, left_time) 
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (uid) DO UPDATE SET 
        is_ban=EXCLUDED.is_ban,
        is_member=EXCLUDED.is_member,
        left_time=EXCLUDED.left_time""", uid, is_ban, True, datetime.now())
        return {"uid": uid, "is_ban": is_ban, "message": "user rejoin success"}
    except Exception as ex:
        log.error("Error occurred when inserting customer record with uid=%s, and exception=%s", uid, ex)
        return None


def update_customer_trade_volumn_by_client(uid):
    request = baseApi(c.ACCESS_KEY, c.SECRET_KEY, c.PASSPHRASE)
    today = datetime.now()
    last_month = today.replace(day=1) - dt.timedelta(days=30)
    epoch_ms = int(last_month.timestamp() * 1000)
    params = {"uid": uid,
              "startTime": str(epoch_ms),
              "endTime": str(utils.get_timestamp()),
              "pageNo": 1,
              "pageSize": 1000
              }
    response = request.post(c.VOLUMN_ENDPOINT, params)
    time.sleep(0.11)
    trade_list = response["data"] if response["data"] else None
    if not trade_list:
        return None
    total_volumn = utils.volumn_calculator(trade_list)
    customer = update_customer_volumn(uid, total_volumn)
    return customer


def update_customer_volumn(uid, volumn):
    try:
        dbconfig.exec_cursor("""
        INSERT INTO erp4btc.customers (uid, trade_volumn) 
        VALUES (%s, %s) 
        ON CONFLICT (uid) DO UPDATE 
        SET trade_volumn=EXCLUDED.trade_volumn""", uid, volumn)
        return {"uid": uid, "trade_volumn": volumn, "message": "trade volumn updated success"}
    except Exception as ex:
        log.error("Error occurred when inserting customer record with uid=%s, and exception=%s", uid, ex)
        return None
