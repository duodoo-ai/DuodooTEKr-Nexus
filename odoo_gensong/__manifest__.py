# -*- coding: utf-8 -*-
{
    'name': "智能仓储集成方案",

    'summary': """
        ERP-WMS-AGV业务接口
    """,

    'description': """智能仓储解决方案
                    更多支持：
                    18951631470
                    zou.jason@qq.com
                    """,

    'author': "Jason Zou",
    "website": "-",

    'category': '中国化应用/智能仓储集成方案',
    'version': '1.0',

    'depends': ['base','mail'],

    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/wms_material_info_views.xml',
        'views/wms_realtime_inventory_views.xml',
        'views/wms_receipt_order_views.xml',
        'views/wms_ship_order_views.xml',
        'views/wms_stock_views.xml',
        'views/wms_category_views.xml',
        'views/wms_unit_views.xml',
        'views/wms_menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    "license": "AGPL-3",
}
