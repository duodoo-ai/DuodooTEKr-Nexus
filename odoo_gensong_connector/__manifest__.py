# -*- coding: utf-8 -*-
{
    'name': "智能仓储集成业务接口",

    'summary': """
        金蝶云星空与井松-WMS-AGV业务接口
    """,

    'description': """金蝶云星空与井松智能仓储解决方案
                    更多支持：
                    18951631470
                    zou.jason@qq.com
                    """,

    'author': "Jason Zou",
    "website": "-",

    'category': '中国化应用/智能仓储集成业务接口',
    'version': '1.0',

    'depends': ['base','mail','odoo_gensong'],

    'data': [
        'data/warehouse_resource_cron.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    "license": "AGPL-3",
}
