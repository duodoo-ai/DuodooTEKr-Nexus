# -*- coding: utf-8 -*-
{
    'name': "Odoo Yunxi API Connector",

    'summary': """
        金蝶云星空采购合同与云玺印管平台审批集成方案
    """,

    'description': """
    金蝶云星空采购合同与云玺印管平台审批集成方案
    1、采购订单单据审核后（流程没结束），调云玺接口，在云玺的系统里生成申请单取得用印授权码，
    2、采购订单这边只有勾选用印的，才需要选择印章名称，用印次数，同时只有勾选用印才需要走接口，回传到单据指定字段，
    3、采购订单传给云玺的信息：发起人，印章名称，日期等
    4、通过云玺印管平台短信接口把订单号，申请人，授权码发送，告诉采购订单的申请人，申请的用印的授权码。  
    更多支持：
    18951631470
    zou.jason@qq.com
    """,

    'author': "Jason Zou",
    "website": "-",

    'category': '中国化应用/云玺印管集成业务接口',
    'version': '1.0',

    'depends': ['base','mail','base_core','base_qstamper'],

    'data': [
        'data/qstamper_resource_cron.xml',
        'data/qstamper_resource_data.xml',
        'security/ir.model.access.csv',
        'views/yunxi_token_views.xml',
        'views/yunxi_menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    "license": "AGPL-3",
}
