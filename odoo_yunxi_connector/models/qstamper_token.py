# -*- coding: utf-8 -*-
"""
@Time    : 2025/1/6 8:20
@Author  : Jason Zou
@Email   : zou.jason@qq.com
@mobile  : 18951631470
"""
import json, time, logging
from odoo import api, fields, models
_logger = logging.getLogger(__name__)

current_time = time.strftime('%Y%m%d%H%M%S', time.localtime())


class YunxiToken(models.Model):
    _name = 'yunxi.token'
    _description = '获取云玺平台接口调用token'

    # 请求内容
    name = fields.Char(string='Auth接口名称', default='获取云玺平台接口调用token', help='API名称')
    appKey = fields.Char(string='应用标识', default='ZYRGroup', help='必填。应用标识')
    appSecret = fields.Char(string='应用秘钥', default='3PUQ4u5w3AQg38OC', help='应用秘钥')
    tenant = fields.Char(string='租户标识', default='zyrg', help='租户标识')
    url = fields.Char(string='接口地址', default='http://58.222.101.110', help='必填。接口地址')
    port = fields.Char(string='接口端口', default='18585', help='接口端口')

    active = fields.Boolean(string='启用', default=True)
    company_id = fields.Many2one(
        'res.company',
        string='公司',
        change_default=True,
        default=lambda self: self.env.company)




