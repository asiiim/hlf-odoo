# -*- coding: utf-8 -*-
{
    'name': "Bank Branch",

    'summary': """
        Managing  multiple bank branches.""",

    'author': "Aashim Bajracharya, 10 Orbits",
    'website': "https://www.10orbits.com/",
    'category': 'Contact',
    'version': '12.0.1.0.0',

    'depends': ['contacts'],

    'data': [
        'security/ir.model.access.csv',
        'views/res_bank_branch.xml',
        'views/res_bank.xml',
        'views/res_partner_bank.xml'
    ],
}