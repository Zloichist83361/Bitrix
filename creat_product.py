from bitrix24 import *
import logging
import sys

logger = logging.getLogger('CREAT_PRODUCT')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('mylog.log', encoding='utf-8')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

products = []

delimiter = ';'
try:
    with open('te1.csv', encoding='utf-8') as f:
        for line in f:
            product = line.split(delimiter)
            products.append(product)
except Exception as e:
    logger.error(f'{e}')
    sys.exit('Stop')

if len(products) < 2:
    logger.info('No correct list')
    sys.exit('Stop')

if len(products[0]) == 13:
    logger.error('No correct size product')
    sys.exit('Stop')

del products[0]

for product in products:
    id = product[0]
    section = product[2]
    section_bitrix_id = ''
    bx24 = Bitrix24('https://b24-jymdkh.bitrix24.ru/rest/1/hu3iszfs1ozy6qwc/')
    if section:
        result = bx24.callMethod('crm.productsection.list', filter={'NAME': section}, select=['ID'])
        logger.debug(f'List product section {result}')

        if result and result[0]:
            section_bitrix_id = result[0].get('ID')
        else:
            section_bitrix_id = bx24.callMethod('crm.productsection.add', fields={'NAME': section})
            logger.debug(f'{section} Add product section')

    result = bx24.callMethod('crm.product.list', filter={'ID': id}, select=['ID'])
    logger.debug(f'List product {result}')

    if result and result[0]:
        update = {'NAME': product[3],
                  'PRICE': product[7],
                  'PROPERTY_137': product[1],
                  'PROPERTY_141': product[4],
                  'PROPERTY_143': product[5],
                  'PROPERTY_145': product[6],
                  'PROPERTY_149': product[9],
                  'PROPERTY_151': product[10],
                  'PROPERTY_153': product[11],
                  'PROPERTY_155': product[12],
                  'SECTION_ID': section_bitrix_id
                  }
        result = bx24.callMethod('crm.product.update', id=id, fields=update)
        logger.info(f'Update product {product[3], product[1]}')
        logger.debug(f'{product[2], product[4], product[5], product[6], product[7], product[8], product[9], product[10], product[11], product[12]}')

    else:
        add = {'ID': id,
               'NAME': product[3],
               'CURRENCY_ID': 'RUB',
               'PRICE': product[7],
               'PROPERTY_137': product[1],
               'PROPERTY_141': product[4],
               'PROPERTY_143': product[5],
               'PROPERTY_145': product[6],
               'PROPERTY_149': product[9],
               'PROPERTY_151': product[10],
               'PROPERTY_153': product[11],
               'PROPERTY_155': product[12],
               'SECTION_ID': section_bitrix_id
               }
        result = bx24.callMethod('crm.product.add', fields=add)
        logger.info(f'Add product {product[3], product[1]}')
        logger.debug(f'{product[2], product[4], product[5], product[6], product[7], product[8], product[9], product[10], product[11], product[12]}')

