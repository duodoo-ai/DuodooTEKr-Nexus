# -*- coding: utf-8 -*-
{
    'name': "Odoo Kingdee Shr Connector",

    'summary': """        
        Odoo and Kingdee e-shr Organizational Structure, 
        Employee Information Integration
        Odoo与金蝶e-shr组织架构、职工信息集成
    """,

    'description': """        
        Odoo and Kingdee e-shr Organizational Structure, 
        Employee Information Integration
        Odoo与金蝶e-shr组织架构、职工信息集成
        More support：
        18951631470
        zou.jason@qq.com
        """,

    'author': "Jason Zou",
    'website': "-",

    'category': 'Base/Shr-Organization',
    'version': '1.0',

    'depends': ['base','hr'],

    'data': [
        'data/eshr_cron.xml',
        'views/hr_department_views.xml',
        'views/hr_employee_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    "license": "AGPL-3",
}
