
from bitrix24 import *
from datetime import datetime
import logging

logger = logging.getLogger('GET_REPORT')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('mylog.log', encoding='utf-8')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

d = datetime.today()

bx24 = Bitrix24('https://b24-jymdkh.bitrix24.ru/rest/1/hu3iszfs1ozy6qwc/')
result = bx24.callMethod('crm.deal.list', filter={'>CREATE_ID': d}, select=['TITLE', 'OPPORTUNITY', 'CURRENCY_ID'])
logger.info(f'List deal {result}')

