# -*- coding: utf-8 -*-
{
    'name': "Partner feature",
    'summary': """
        Set Defoult Company and Add Bank Branch Field.
    """,
    'sequence': '1',
    'description': """
        Features:
        \n- Set Company Default and Bank Branch.
    """,
    'author': "Dharmajit Budha",
    'company': 'Ten Orbits Pvt. Ltd.',
    'website': "https://www.10orbits.com/",
    'category': 'Contacts',
    'version': '14.0.0.0.1',
    'application': True,
    'depends': ['bank_branch','account'],
    'data': [
        'views/res_partner.xml'
    ],
}