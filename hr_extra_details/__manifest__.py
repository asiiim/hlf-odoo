# -*- coding: utf-8 -*-
{
    'name': "HR Extra Details",

    'summary': """
        HR and Contract Related Detail Info.""",

    'author': "Manoj Khadka, 10 Orbits",
    'website': "https://www.10orbits.com/",
    'category': 'Contact',
    'version': '14.0.1.0.0',

    'depends': ['bank_branch','hr_contract'],

    'data': [
        'security/ir.model.access.csv',
        'views/hr_extra_details.xml'
    ],
}