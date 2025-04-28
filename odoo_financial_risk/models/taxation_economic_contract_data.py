# Copyright 2025 多度信息科技（南京）有限公司 (DuodooTEKr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# -*- coding: utf-8 -*-
"""
@Time    : 2025/04/08 18:05
@Author  : Jason Zou
@Email   : zou.jason@qq.com
@Mobile  : 18951631470
"""
from odoo import models, fields

class EconomicContractDataCollection(models.Model):
    _name = 'economic.contract.data'
    _inherit = ['mail.thread']
    _description = '经法合同数据模板'

    name = fields.Char(string="合同名称", required=True)
    code = fields.Char(string='合同编号')
    contract_code = fields.Char(string='统一合同文本编码')
    contract_category = fields.Many2one('base.contract.category', string='合同分类及名称*', ondelete='restrict')
    contract_organizer = fields.Many2one('base.contract.organizer', string='合同承办单位*', ondelete='restrict')
    contract_opposing = fields.Many2one('base.contract.opposing', string='对方单位名称*', ondelete='restrict')
    date_signing = fields.Date(string='签订日期*')
    contract_amount = fields.Float(string='合同金额*', digits='Amount')
    contract_amount_exclude_tax = fields.Float(string='合同不含税金额*', digits='Amount')
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        change_default=True,
        default=lambda self: self.env.company)