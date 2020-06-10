from bitrix24 import *

products = []
with open('test.csv', encoding='utf-8') as f:
    for line in f:
        product = line.split(';')
        products.append(product)

del products[0]

for product in products:
    id = product[0]
    section = product[2]
    section_bitrix_id = ''
    bx24 = Bitrix24('REST_BITRIX')
    if section:
        result = bx24.callMethod('crm.productsection.list', filter={'NAME': section}, select=['ID'])
        if result and result[0]:
            section_bitrix_id = result[0].get('ID')
        else:
            section_bitrix_id = bx24.callMethod('crm.productsection.add', fields={'NAME': section})

    result = bx24.callMethod('crm.product.list', filter={'ID': id}, select=['ID'])
    if result and result[0]:
        result = bx24.callMethod('crm.product.update', id=id, fields={'NAME': product[3],
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
                                                                    })
    else:
        result = bx24.callMethod('crm.product.add', fields={'ID': id,
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
                                                            })

