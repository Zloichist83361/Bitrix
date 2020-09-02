from bitrix24 import *
import logging
from datetime import datetime
import sentry_sdk

sentry_sdk.init("https://9bb20182388f4a05a93b80a15c333130@o419540.ingest.sentry.io/5334036")

logger = logging.getLogger('GET_REPORT')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('my_log.log', encoding='utf-8')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

date_create = datetime.now().date()


def create_deal():
    try:
        tg_sales = ''
        bx24 = Bitrix24('https://b24-jymdkh.bitrix24.ru/rest/1/hu3iszfs1ozy6qwc/')
        result_sales = bx24.callMethod('crm.deal.list', filter={'>DATE_CREATE': date_create},
                                       select=['TITLE', 'OPPORTUNITY', 'CURRENCY_ID'])
        logger.info(f'List deal {result_sales}')
        for sales in result_sales:
            tg_sales += sales['TITLE'] + ' ' + sales['OPPORTUNITY'] + ' ' + sales['CURRENCY_ID'] + '\n'
        return tg_sales
    except KeyError as e:
        logger.error(e)
        sentry_sdk.capture_exception(error=e)


def create_all_sum_deal():
    try:
        tg_all_sum = []
        bx24 = Bitrix24('https://b24-jymdkh.bitrix24.ru/rest/1/hu3iszfs1ozy6qwc/')
        result_sales = bx24.callMethod('crm.deal.list', filter={'>DATE_CREATE': date_create},
                                       select=['TITLE', 'OPPORTUNITY', 'CURRENCY_ID'])
        logger.info(f'List all sum {result_sales}')
        for sales in result_sales:
            tg_all_sum.append(sales['OPPORTUNITY'])
        return tg_all_sum
    except KeyError as e:
        logger.error(e)
        sentry_sdk.capture_exception(error=e)


def create_lead():
    try:
        tg_leads = ''
        bx24 = Bitrix24('https://b24-jymdkh.bitrix24.ru/rest/1/hu3iszfs1ozy6qwc/')
        result_leads = bx24.callMethod('crm.lead.list', filter={'>DATE_CREATE': date_create},
                                       select=['TITLE', 'OPPORTUNITY', 'CURRENCY_ID'])
        logger.info(f'List lead {result_leads}')
        for leads in result_leads:
            tg_leads += leads['TITLE'] + ' ' + leads['OPPORTUNITY'] + ' ' + leads['CURRENCY_ID'] + '\n'
        return tg_leads
    except KeyError as e:
        logger.error(e)
        sentry_sdk.capture_exception(error=e)
