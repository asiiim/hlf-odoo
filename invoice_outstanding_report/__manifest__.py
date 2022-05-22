# -*- coding: utf-8 -*-

{
    'name': "Outstanding Invoice Report",
    'author': 'Ascetic Business Solution',
    'category': 'account_invoicing',
    'summary': """Report for customer's outstanding invoice amount within the particular date period""",
    'website': 'http://www.asceticbs.com',
    'license': 'AGPL-3',
    'description': """
""",
    'version': '14.0.0.1',
    'depends': ['base','account','report_xlsx'],
    'data': [
        'wizard/invoice_outstanding_wiz.xml',
        'security/ir.model.access.csv',
        'views/invoice_outstanding_report_view.xml',
        'report/invoice_outstanding_template.xml',
        'report/invoice_outstanding_report.xml'],
    'installable': True,
    'images': ['static/description/banner.png'],
    'application': True,
    'auto_install': False,
}
