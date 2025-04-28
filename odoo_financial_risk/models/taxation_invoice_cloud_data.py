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

class InvoiceConstructionCloud(models.Model):
    _name = 'invoice.construction.cloud'
    _inherit = ['mail.thread']
    _description = '已勾选发票 智税云导出（月底比对账面除旅客运输外的进项税）'

    name = fields.Char(string="发票号码")
    invoice_status = fields.Char(string='发票状态')
    check_identification = fields.Char(string='查验标识')
    authentication_type = fields.Char(string='认证类型')
    reason_non_deduction = fields.Char(string='不抵扣原因')
    check_result = fields.Char(string='勾选结果')
    check_date = fields.Date(string='勾选日期')
    check_person = fields.Char(string='勾选人')
    invoice_code = fields.Char(string='发票代码')
    invoice_date = fields.Date(string='开票日期')
    excluding_tax_amount = fields.Float(string='不含税金额', digits='Amount')
    tax_rate = fields.Float(string='税率', digits=(9, 2))
    tax_amount = fields.Float(string='税额', digits='Amount')
    deductible_tax_amount = fields.Float(string='可抵扣税额', digits='Amount')
    subtotal_amount = fields.Float(string='价税合计', digits='Amount')
    product_name = fields.Char(string='商品名称')
    buyers_name = fields.Char(string='购买方名称')
    buyers_tax = fields.Char(string='购买方税号')
    seller_name = fields.Char(string='销售方名称')
    seller_tax = fields.Char(string='销售方税号')
    note = fields.Char(string='备注')
    receiver = fields.Char(string='收管人')
    transferor = fields.Char(string='移交人')
    receiver_date = fields.Date(string='收管日期')
    invoice_purpose = fields.Char(string='发票用途')
    voucher_code = fields.Char(string='凭证编号')
    voucher_date = fields.Date(string='制证日期')
    voucher_type = fields.Char(string='发票类型')
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        change_default=True,
        default=lambda self: self.env.company)