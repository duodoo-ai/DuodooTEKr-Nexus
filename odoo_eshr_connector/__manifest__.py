# -*- coding: utf-8 -*-
{
    'name': "Odoo Kingdee Shr Connector",

    'summary': """
        Odoo与金蝶e-shr组织架构、职工信息集成
    """,

    'description': """Odoo与金蝶e-shr组织架构、职工信息集成
                    更多支持：
                    18951631470
                    zou.jason@qq.com
                    """,

    'author': "Jason Zou",
    'website': "www.duodoo.tech",

    'category': '中国化应用/金蝶组织架构集成',
    'version': '1.0',

    'depends': ['base','hr'],

    'data': [
        'views/hr_department_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    "license": "AGPL-3",
}
