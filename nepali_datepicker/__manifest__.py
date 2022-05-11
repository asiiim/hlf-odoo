# -*- coding: utf-8 -*-
# Part of 10 Orbits Pvt. Ltd. See LICENSE for full copyright and licensing details.

{
    'name' : 'Nepali Datepicker (Calendar)',
    'version' : '14.0.0.0.1',
    'summary': 'Nepali Datepicker for all Odoo modules, with instant AD to BS and BS to AD conversions',
    'sequence': 1,
    'category': 'Localization',
    'description': """
        Nepali Calendar
        ====================================
        Includes:
        1. Nepali Datepicker for all modules
        2. Abstract method to convert English date to Nepali Date
    """,
    'website': 'https://erp.10orbits.com',
    'images' : ['static/description/banner.png'],
    'depends' : ['base', 'web','base_setup'],
    'external_dependencies': {'python': ['nepali_datetime']},
    'author': 'Aashim Bajracharya',
    'company': 'Ten Orbits Pvt. Ltd.',
    'data': [
        'views/assets.xml',
        'views/css.xml',
        'views/res_config_settings.xml'
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
    'sequence': 1,
    'auto_install': False,
    'price': 150,
    'currency': 'USD',
    'license': 'OPL-1',
}
