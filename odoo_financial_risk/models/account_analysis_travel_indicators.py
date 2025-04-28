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

class AnalysisBusinessTravelIndicator(models.Model):
    _name = 'account.analysis.travel.indicator'
    _inherit = ['mail.thread']
    _description = '商旅指标分析'

    name = fields.Many2one('base.technical.committees', string='归口单位', ondelete='restrict')
    receipt_voucher = fields.Char(string='指标要求')
    receipt_date = fields.Date(string='入账时间')
    project_ids = fields.Many2one(
        'account.business.travel.items',
        string='商旅指标项目',
        ondelete='cascade'
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        change_default=True,
        default=lambda self: self.env.company)