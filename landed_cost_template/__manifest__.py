{
    'name': 'Landed Cost Template',
    'version': '14.0.0.0.1',
    'category': 'Purchase',
    'summary': 'Select the set of landed cost template for the purchase bill documents.',
    'sequence': '1',
    'author': 'Ten Orbits Pvt. Ltd.',
    'maintainer': 'Aashim Bajracharya',
    'website': 'https://www.10orbits.com/',
    'depends': ['stock', 'stock_landed_costs'],
    'data': [
        'security/ir.model.access.csv',
        'views/landed_cost_template.xml',
        'views/vendor_bill.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
