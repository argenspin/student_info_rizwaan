{
    'name': "Students",
    'version': "14.0.1.0",
    'sequence': "0",
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/student_details_views.xml',
        'report/student_result_report.xml',
    ],
    # 'assets':{
    #     'web.assets_backend': [

    #     ]
    # },
    'demo': [],
    'summary': "Students",
    'description': "",
    'installable': True,
    'auto_install': False,
    'license': "LGPL-3",
    'application': True
}