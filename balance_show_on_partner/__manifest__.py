# -*- coding: utf-8 -*-
{
    'name': "Balance Show on Partner Select",

    'summary': """
        Balance Show on Partner Select in Sales/Purchase/Invoice/Bill""",

    'author': "Manoj Khadka, 10 Orbits",
    'website': "https://www.10orbits.com/",
    'category': 'Contact',
    'version': '14.0.1.0.0',

    'depends': ['sale','purchase','account'],

    'data': [
        'views/balance_show_on_invoice.xml',
        'views/balance_show_on_purchase.xml',
        'views/balance_show_on_sale.xml'
    ],
}