# -*- coding: utf-8 -*-

{
    'name': 'HR Data API',
    'version': '14.0.1.0.0',
    'category': 'Human Resources',
    'summary': """
        HR related additional data to be dumped through REST API.
    """,
    'description': """
        \n- Add field 'joining_date' in hr.employee.
    """,
    'author': 'Aashim Bajracharya',
    'company': 'Ten Orbits Pvt. Ltd.',
    'maintainer': 'Aashim Bajracharya',
    'website': 'https://10orbits.com',
    'depends': ['hr', 'hr_contract', 'res_district'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/hr_employee.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': 1,
    'license': 'AGPL-3',
}