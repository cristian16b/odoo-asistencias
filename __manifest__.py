{
    'name': 'Department Attendance Wizard',
    'version': '1.0',
    'category': 'Human Resources',
    'summary': 'Registrar asistencias por departamento',
    'depends': ['hr','hr_attendance'],
    'data': [
        'views/department_attendance_wizard_views.xml',
        'views/department_attendance_line_views.xml',
        'views/department_attendance_action.xml',
        'views/department_attendance_menu.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
}