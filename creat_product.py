from bitrix24 import *
import logging
import sys
import sentry_sdk
import glob
import os

sentry_sdk.init("https://9bb20182388f4a05a93b80a15c333130@o419540.ingest.sentry.io/5334036")

logger = logging.getLogger('CREAT_PRODUCT')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('my_log.log', encoding='utf-8')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

products = []
delimiter = ';'


def check_section(product):
    section = product[2]
    bx24 = Bitrix24('https://b24-3xzo32.bitrix24.ru/rest/1/szrks03x762pgphu/profile/')
    section_id_bitrix = bx24.callMethod('crm.productsection.list', filter={'NAME': section}, select=['ID'])
    logger.debug(f'List product section {section_id_bitrix}')
    return section_id_bitrix


def check_product(product):
    id = product[0]
    bx24 = Bitrix24('https://b24-3xzo32.bitrix24.ru/rest/1/szrks03x762pgphu/profile/')
    result = bx24.callMethod('crm.product.list', filter={'PROPERTY_125': id}, select=['ID'])
    logger.debug(f'List product {result}')
    return result


def create_section(product):
    section = product[2]
    bx24 = Bitrix24('https://b24-3xzo32.bitrix24.ru/rest/1/szrks03x762pgphu/profile/')
    section_bitrix = bx24.callMethod('crm.productsection.add', fields={'NAME': section})
    logger.debug(f'Add product section {section}')
    return section_bitrix


def update_product(product, section_id, product_id):
    bx24 = Bitrix24('https://b24-3xzo32.bitrix24.ru/rest/1/szrks03x762pgphu/profile/')
    result = bx24.callMethod('crm.product.update', id=product_id, fields={'NAME': product[3],
                                                                          'PRICE': product[7],
                                                                          'PROPERTY_103': product[1],  # Штрихкод
                                                                          'PROPERTY_105': product[2],
                                                                          # Группа товаров
                                                                          'PROPERTY_107': product[4],  # Размер
                                                                          'PROPERTY_109': product[5],  # Цвет
                                                                          'PROPERTY_111': product[6],  # Остаток
                                                                          'PROPERTY_113': product[9],  # Артикул
                                                                          'PROPERTY_115': product[10],
                                                                          # Страна-производитель
                                                                          'PROPERTY_117': product[11],  # Код товара
                                                                          'PROPERTY_119': product[12],  # Атрибут4
                                                                          'SECTION_ID': section_id
                                                                          })
    logger.info(f'Update product {product[3], product[1]}')
    logger.debug(
        f'{product[2], product[4], product[5], product[6], product[7], product[8], product[9], product[10], product[11], product[12]}')
    return result


def create_product(product, section_id):
    id = product[0]
    bx24 = Bitrix24('https://b24-3xzo32.bitrix24.ru/rest/1/szrks03x762pgphu/')
    result = bx24.callMethod('crm.product.add', fields={'NAME': product[3],
                                                        'CURRENCY_ID': 'RUB',
                                                        'PRICE': product[7],
                                                        'PROPERTY_103': product[1],  # Штрихкод
                                                        'PROPERTY_105': product[2],  # Группа товаров
                                                        'PROPERTY_107': product[4],  # Размер
                                                        'PROPERTY_109': product[5],  # Цвет
                                                        'PROPERTY_111': product[6],  # Остаток
                                                        'PROPERTY_113': product[9],  # Артикул
                                                        'PROPERTY_115': product[10],
                                                        # Страна-производитель
                                                        'PROPERTY_117': product[11],  # Код товара
                                                        'PROPERTY_119': product[12],  # Атрибут4
                                                        'SECTION_ID': section_id,
                                                        'PROPERTY_125': id  # ID csv
                                                        })
    logger.info(f'Add product {product[3], product[1]}')
    logger.debug(
        f'{product[2], product[4], product[5], product[6], product[7], product[8], product[9], product[10], product[11], product[12]}')
    return result


def create_products_from_csv():
    try:
        files_path = os.path.join('Ftp_download', '*')
        files = sorted(glob.iglob(files_path), key=os.path.getctime, reverse=True)
        with open(files[0], encoding='utf-8') as f:
            for line in f:
                product = line.split(delimiter)
                products.append(product)
                if len(products) == 13:
                    logger.info('No correct list')
                    sys.exit('Stop')
                for product in products[1:]:
                    section_bitrix = check_section(product)
                    if not section_bitrix:
                        section_id = create_section(product)
                        logger.info(f'Not section_id{section_id}')
                    else:
                        section_id = section_bitrix[0].get('ID')
                        logger.info(f'Yes section_id{section_id}')
                    bitrix = check_product(product)
                    if not bitrix:
                        create_product(product, section_id)
                    else:
                        update_product(product, section_id, bitrix[0]['ID'])
    except FileNotFoundError as e:
        logger.error(e)
        sentry_sdk.capture_exception(error=e)
    except OSError as e:
        logger.error(e)
        sentry_sdk.capture_exception(error=e)
