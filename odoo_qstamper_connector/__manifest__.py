# -*- coding: utf-8 -*-
{
    'name': "云玺印管集成业务接口(文件受控)",

    'summary': """
        金蝶云星空销售合同通过第三方业务接口增加“受控”水印并通过接口反馈回金蝶云星空附件集成方案
    """,

    'description': """
    金蝶云星空销售合同通过第三方业务接口增加“受控”水印并通过接口反馈回金蝶云星空附件集成方案
    更多支持：
    18951631470
    zou.jason@qq.com
    """,

    'author': "Jason Zou",
    "website": "www.duodoo.tech",

    'category': '中国化应用/云玺印管集成业务接口',
    'version': '1.0',

    'depends': ['base','mail','base_qstamper'],

    'data': [
        'data/qstamper_resource_cron.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    "license": "AGPL-3",
}
