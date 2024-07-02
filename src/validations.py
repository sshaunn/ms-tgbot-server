from datetime import datetime, date

from src.service.customer_service import get_customer_by_uid, update_customer_trade_volumn_by_client


def is_valid_uid(customer):
    return customer is not None


def is_exist_uid(uid):
    customer = get_customer_by_uid(uid)
    if customer:
        if not customer['is_ban'] or customer['is_member']:
            return True
    return False


def is_ban(start_time):
    start_date = datetime.strptime(start_time.isoformat(), "%Y-%m-%d").date()
    return (date.today() - start_date).days >= 30


def is_over_trade_volumn(uid):
    customer = update_customer_trade_volumn_by_client(uid)
    return customer['trade_volumn'] >= 10000
