# -*- coding: utf-8 -*-
{
    'name': "Odoo Financial Risk(RTX)",

    'summary': """
        Smart Financial Risk Prevention and Control Service System
    """,

    'description': """
    智慧财务风险防控服务系统
    更多支持：
    18951631470
    zou.jason@qq.com
    """,

    'author': "Jason Zou",
    "website": "-",

    'category': 'financial (Frisk)',
    'version': '1.0',

    'depends': ['base','mail'],

    'data': [
        'data/dues_risk_data.xml',
        'data/financial_risk_data.xml',
        'data/account_risk_data.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
        'wizard/project_selection_wizard_view.xml',
        'views/base_data_views.xml',
        'views/taxation_economic_contract_data_views.xml',
        'views/taxation_daily_research_develop_views.xml',
        'views/taxation_invoice_cloud_data_views.xml',
        'views/account_analysis_supplier_outside_views.xml',
        'views/account_analysis_travel_indicator_views.xml',
        'views/dues_income_expenditure_views.xml',
        'views/base_menu_views.xml',
    ],
    'assets': {
            'web.assets_backend': [
                'odoo_financial_risk/static/src/css/custom_kanban.css',
            ],
        },
    'demo': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    "license": "AGPL-3",
}
