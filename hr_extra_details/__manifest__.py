# -*- coding: utf-8 -*-
{
    'name': "HR Extra Details",

    'summary': """
        HR and Contract Related Detail Info.""",

    'author': "Manoj Khadka, 10 Orbits",
    'maintainer': "Aashim Bajracharya",
    'website': "https://www.10orbits.com/",
    'category': 'HR',
    'version': '14.0.0.0.1',
    'sequence': 1,
    'application': True,
    'depends': ['bank_branch','hr_contract', 'res_district'],

    'data': [
        'security/ir.model.access.csv',
        'views/hr_extra_details.xml',
        'views/hr_employee.xml',
        'views/hr_contract.xml'
    ],
}