import os
from pathlib import Path

import yaml

from dotenv import load_dotenv, find_dotenv
from typing import Final

project_root = Path(__file__).parent.parent

# Construct the path to the yaml file
yaml_path = project_root / 'resource' / 'application.yaml'

load_dotenv(find_dotenv())


# def configure():
with open(yaml_path, 'r') as f:
    config = yaml.safe_load(f)


# env variables
ENV: Final = os.environ.get('ENV')
TOKEN: Final = os.environ.get('TOKEN')
USERNAME: Final = os.environ.get('USERNAME')
ACCESS_KEY: Final = os.environ.get('ACCESS_KEY')
SECRET_KEY: Final = os.environ.get('SECRET_KEY')
PASSPHRASE: Final = os.environ.get('PASSPHRASE')

PORT: Final = config['server']['port']

# endpoint
# BASE_URL: Final = config['service']['bit-get']['baseUrl']
AGENT_ENDPOINT: Final = config['service']['bit-get']['endpoint']['customer-list']
VOLUMN_ENDPOINT: Final = config['service']['bit-get']['endpoint']['customer-trade-volumn']
# SERVER_TIME_ENDPOINT: Final = config['service']['bit-get']['endpoint']['server-time']

TELEGRAM_API_PREFIX: Final = f"{config['service']['telegram']['base-url']}bot{TOKEN}"

# http header
CONTENT_TYPE: Final = 'Content-Type'
OK_ACCESS_KEY: Final = 'ACCESS-KEY'
OK_ACCESS_SIGN: Final = 'ACCESS-SIGN'
OK_ACCESS_TIMESTAMP: Final = 'ACCESS-TIMESTAMP'
OK_ACCESS_PASSPHRASE: Final = 'ACCESS-PASSPHRASE'
APPLICATION_JSON: Final = 'application/json'

# header key
LOCALE: Final = 'locale'

# method
GET: Final = "GET"
POST: Final = "POST"
DELETE: Final = "DELETE"

# sign type
RSA: Final = "RSA"
SHA256: Final = "SHA256"
SIGN_TYPE: Final = SHA256

# database
DATABASE_NAME: Final = 'uidList_database.csv'
DBHOST: Final = config['service']['database']['host']
DBPORT: Final = config['service']['database']['port']
DBNAME: Final = config['service']['database']['dbname']
DB_USERNAME: Final = config['service']['database']['username']
DB_PASSWORD: Final = config['service']['database']['password']
DBHOST_PROD: Final = config['service']['database']['prod']['host']
DBPORT_PROD: Final = config['service']['database']['prod']['port']
DBNAME_PROD: Final = config['service']['database']['prod']['dbname']
DB_USERNAME_PROD: Final = config['service']['database']['prod']['username']
DB_PASSWORD_PROD: Final = config['service']['database']['prod']['password']

# tg group id
EFFECTIVE_CHAT_ID: Final = '-1002087737560'
# VIP_GROUP_ID: Final = '-1001856345480'
VIP_GROUP_ID: Final = config['service']['telegram']['test-group-id']
PRIVATE_GROUP_ID: Final = '-1002043576596'
TEST_GROUP_ID: Final = config['service']['telegram']['test-group-id']

FINISH_CONVERSATION_MESSAGE: Final = """已终止对话,感谢关注,祝您交易顺利!"""

SUCCESS_MESSAGE_UID_CHECK: Final = """您已验证成功!感谢关注!"""
SUCCESS_MESSAGE_REJOIN: Final = """"""

ERROR_MESSAGE_FROM_BOT_REJOIN: Final = """未达到入群资格,如有疑问请咨询群主或管理,本次对话结束,感谢使用"""
ERROR_MESSAGE_FROM_BOT: Final = """UID不正确,本次对话结束,如需重新验证,请输入'/check'重新验证"""
ERROR_MESSAGE_FROM_BOT_USER_EXIST: Final = """UID已验证过,无须再次验证,本次对话结束,感谢使用,祝交易顺利!"""
ERROR_MESSAGE_FROM_BOT_USER_BANNED: Final = """您因当月交易额未满一万USDT被移出交易群组,如有疑问请咨询群主或管理,本次对话结束,感谢使用,
祝交易顺利!"""
ERROR_MESSAGE_FROM_BOT_DUPLICATED_UID_CHECK: Final = """您已验证过,无须再次验证!感谢使用"""
