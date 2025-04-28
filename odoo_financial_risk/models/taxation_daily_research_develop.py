# Copyright 2025 多度信息科技（南京）有限公司 (DuodooTEKr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# -*- coding: utf-8 -*-
"""
@Time    : 2025/04/08 18:05
@Author  : Jason Zou
@Email   : zou.jason@qq.com
@Mobile  : 18951631470
"""
from odoo import models, fields, api

class DailyResearchDevelopDeduct(models.Model):
    _name = 'daily.research.develop.deduct'
    _inherit = ['mail.thread']
    _description = '日常研发加计扣除'

    name = fields.Char(string="项目名称", required=True)
    project_code = fields.Char(string="项目编码")
    sequence = fields.Integer(string='序号', default=1)
    technical_committees = fields.Many2one('base.technical.committees', string='归口单位', ondelete='restrict')
    entrusted_committees = fields.Many2one('base.entrusted.committees', string='受托单位名称', ondelete='restrict')
    related_partner = fields.Selection([
        ('是', '是'),
        ('否', '否')
    ], string='是否关联方')
    technological_partner = fields.Selection([
        ('是', '是'),
        ('否', '否')
    ], string='是否认定为技术开发合同')
    budget_amount = fields.Float(string='预算金额（万元）', digits='Amount')
    invoice_amount_exclude_tax = fields.Float(string='开票不含税金额（万元）', digits='Amount', help='按受托单位对应填报')
    related_entrusted_auxiliary_amount_1 = fields.Float(string='关联方受托辅助账1-5项合计（万元）', digits='Amount')
    related_entrusted_auxiliary_amount_2 = fields.Float(string='关联方受托辅助账第6项合计（万元）', digits='Amount')
    note = fields.Html(string='备注')
    active = fields.Boolean(string='启用', default=True, help='行数据不纳入统计，处理于失效状态!')
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        change_default=True,
        default=lambda self: self.env.company)

    @api.model
    def create(self, vals):
        last_record = self.search([], order='sequence desc', limit=1)
        if last_record:
            new_sequence = last_record.sequence + 1
        else:
            new_sequence = 1
        vals['sequence'] = new_sequence
        return super(DailyResearchDevelopDeduct, self).create(vals)


class DailyResearchDevelopList(models.Model):
    _name = 'daily.research.develop.list'
    _inherit = ['mail.thread']
    _description = '日常研发加计扣除清单'

    name = fields.Many2one('daily.research.develop.deduct', string="项目名称", required=True, ondelete='restrict')
    project_code = fields.Char(related='name.project_code', string="项目编码")
    sequence = fields.Integer(string='序号', default=1)
    technical_committees = fields.Many2one(related='name.technical_committees', string='归口单位', ondelete='restrict')
    entrusted_committees = fields.Many2one(related='name.entrusted_committees', string='受托单位名称', ondelete='restrict')
    related_partner = fields.Selection(related='name.related_partner', string='是否关联方')
    technological_partner = fields.Selection(related='name.technological_partner', string='是否认定为技术开发合同')
    budget_amount = fields.Float(related='name.budget_amount', string='预算金额（万元）', digits='Amount')
    invoice_amount_exclude_tax = fields.Float(related='name.invoice_amount_exclude_tax', string='开票不含税金额（万元）', digits='Amount', help='按受托单位对应填报')
    related_entrusted_auxiliary_amount_1 = fields.Float(related='name.related_entrusted_auxiliary_amount_1', string='关联方受托辅助账1-5项合计（万元）', digits='Amount')
    related_entrusted_auxiliary_amount_2 = fields.Float(related='name.related_entrusted_auxiliary_amount_2', string='关联方受托辅助账第6项合计（万元）', digits='Amount')
    note = fields.Html(related='name.note', string='备注')
    active = fields.Boolean(string='启用', default=True, help='行数据不纳入统计，处理于失效状态!')
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        change_default=True,
        default=lambda self: self.env.company)

    @api.model
    def create(self, vals):
        last_record = self.search([], order='sequence desc', limit=1)
        if last_record:
            new_sequence = last_record.sequence + 1
        else:
            new_sequence = 1
        vals['sequence'] = new_sequence
        return super(DailyResearchDevelopList, self).create(vals)

    period_date = fields.Date(string='业务时间')
    voucher_type = fields.Selection([
        ('转账凭证', '转账凭证'),
        ('收款凭证', '收款凭证'),
        ('付款凭证', '付款凭证'),
    ], string='凭证类型', default='转账凭证')
    voucher_code = fields.Char(string='转账凭证号', )

    period_date_2 = fields.Date(string='付款时间')
    payment_voucher_type = fields.Selection([
        ('转账凭证', '转账凭证'),
        ('收款凭证', '收款凭证'),
        ('付款凭证', '付款凭证'),
    ], string='付款凭证类型', default='付款凭证')
    payment_voucher_code = fields.Char(string='付款凭证号', )
    payment_amount = fields.Float(string='支付金额（万元）', digits='Amount')
    digital_code = fields.Char(string='数电票票号', )
    payment_part = fields.Selection([
        ('是', '是'),
        ('否', '否')
    ], string='存在一张发票部分支付', default='否')