# -*- coding: utf-8 -*-

{
    'name': 'District Information',
    'version': '14.0.0.0.1',
    'category': 'Base',
    'summary': """
        District information in a state of a country.
    """,
    'description': """
        \n- Create a district data in state of a country.
    """,
    'author': 'Aashim Bajracharya',
    'company': 'Ten Orbits Pvt. Ltd.',
    'maintainer': 'Aashim Bajracharya',
    'website': 'https://10orbits.com',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_district.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': 1,
    'license': 'AGPL-3',
}