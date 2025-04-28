# Copyright 2025 多度信息科技（南京）有限公司 (DuodooTEKr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# -*- coding: utf-8 -*-
"""
@Time    : 2025/04/10 18:05
@Author  : Jason Zou
@Email   : zou.jason@qq.com
@Mobile  : 18951631470
"""
from odoo import models, fields

class AnalysisSupplierOutside(models.Model):
    _name = 'analysis.supplier.outside'
    _inherit = ['mail.thread']
    _description = '系统外供应商情况分析'

    name = fields.Selection([
        ('地方政府部门', '地方政府部门'),
        ('国资委管理的中央企业', '国资委管理的中央企业'),
        ('财政部、中央汇金公司管理的中央企业', '财政部、中央汇金公司管理的中央企业'),
        ('国务院其他部门或群众团体管理的中央企业', '国务院其他部门或群众团体管理的中央企业'),
        ('地方国有企业', '地方国有企业'),
        ('民营企业', '民营企业'),
        ('集体所有制企业', '集体所有制企业'),
        ('中央政府部门', '中央政府部门'),
        ('个人', '个人'),
        ('其他', '其他')
    ], string='企业性质')
    private_owned = fields.Selection([
        ('是', '是'),
        ('否', '否')
    ], string='是否民营', default='否')
    receipt_voucher = fields.Char(string='入账凭证')
    receipt_date = fields.Date(string='入账时间')
    receipt_amount = fields.Float(string='入账金额', digits='Amount')
    payment_voucher = fields.Char(string='支付凭证')
    payment_date = fields.Date(string='支付时间')
    payment_amount = fields.Float(string='支付金额', digits='Amount')
    contract_completion_period = fields.Date(string='合同完成周期', help='合同完成周期（xx月）')
    excluding_tax_amount = fields.Float(string='不含税金额', digits='Amount')
    contract_completion_rate = fields.Float(string='合同前完成准时率', digits=(9, 2))
    ranking_incoming_amount = fields.Integer(string='入账金额排名')
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        change_default=True,
        default=lambda self: self.env.company)