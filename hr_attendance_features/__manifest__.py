{
    'name': 'HR Attendance Features',
    'version': '14.0.0.0.1',
    'category': 'HR',
    'summary': 'Extra features related to HR Attendance.',
    'description': """
        Features:
        \n- Attendance monthly report.
    """,
    'sequence': '1',
    'author': 'Ten Orbits Pvt. Ltd.',
    'website': 'https://www.10orbits.com/',
    'depends': ['hr_attendance', 'generic_qweb_templates', 'resource'],
    'data': [
        'security/ir.model.access.csv',
        'reports/hr_attendance.xml',
        'wizards/attendance_report.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
