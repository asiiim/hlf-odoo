# -*- coding: utf-8 -*-
# Part of 10 Orbits Pvt. Ltd. See LICENSE for full copyright and licensing details.

{
    'name' : 'Nepali Datepicker (Calendar)',
    'version' : '1.0',
    'summary': 'Nepali Datepicker for all Odoo modules, with instant AD to BS and BS to AD conversions',
    'sequence': 16,
    'category': 'Localization',
    'description': """
Nepali Calendar
====================================
Includes:
1. Nepali Datepicker for all modules
    """,
    'website': 'https://erp.10orbits.com',
    'images' : ['static/description/banner.png'],
    'depends' : ['base', 'web'],
    'author': '10 Orbits',
    'company': '10 Orbits',
    'data': [
        'views/assets.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'price': 150,
    'currency': 'USD',
    'license': 'OPL-1',
}
