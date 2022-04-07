# -*- coding: utf-8 -*-
{
    'name': "Generic Qweb Templates",

    'summary': """
        List of generic qweb templates.
    """,
    "description": """
        Features:
        \n- Amount in Words
        \n- Semi Footer Information
        \n- Document Title
        \n- Custom layouts

    """,
    'sequence': '1',
    'author': "Ten Orbits Pvt. Ltd.",
    'website': "10orbits.com",
    'category': 'Reports',
    'version': '14.0.0.0.2',

    'depends': [
        'base'
    ],

    'data': [
        'reports/abstract_templates.xml',
        'reports/custom_layouts.xml'
    ],

    'application': True
}