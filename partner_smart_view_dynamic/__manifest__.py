
{
    'name': 'Ledger View In Partner',
    'summary': 'Adds smart button to view general ledger from contact',
    'description': '''
This module provide smart clickable button in partner through which general ledger can be viewed directly ''',
    'author': 'Manoj khadka',
    'version': '14.0.1.0.0',
    'category': 'Accounting/Accounting',
    'depends': [
        'base','account','account_dynamic_reports','nepali_datepicker'
    ],
    
    'qweb': [
        'static/src/xml/smart_view_dynamic.xml',
        'static/src/xml/dynamic_np_date.xml',

    ],
    'data': [
        'views/smart_view_dynamic_view.xml',
        'views/dynamic_np_date_pdf.xml',
    ],
   
    'installable': True,
    'application': False,
}

