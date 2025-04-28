# Copyright 2025 多度信息科技（南京）有限公司 (DuodooTEKr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# -*- coding: utf-8 -*-
"""
@Time    : 2025/04/10 18:05
@Author  : Jason Zou
@Email   : zou.jason@qq.com
@Mobile  : 18951631470
"""
from odoo import models, fields, api

class DuesIncomeExpenditure(models.Model):
    _name = 'dues.income.expenditure'
    _inherit = ['mail.thread']
    _description = '年度党费收支、结存情况表'

    name = fields.Char(string='填报单位')
    statistical_date = fields.Date(string='统计时间')
    line_ids = fields.One2many(
        'dues.income.expenditure.line',  # 关联从表模型
        'due_id',  # 对应从表的 Many2one 字段名
        string='明细行',
        tracking=True  # 启用变更追踪（可选）
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        change_default=True,
        default=lambda self: self.env.company)

    total_subtotal = fields.Float(
        string='总金额',
        compute='_compute_total_subtotal',
        store=True
    )
    total_current_amount = fields.Float(
        string='本级总金额',
        compute='_compute_total_subtotal',
        store=True
    )
    total_next_amount = fields.Float(
        string='下一级总金额',
        compute='_compute_total_subtotal',
        store=True
    )

    @api.depends('line_ids.subtotal')
    def _compute_total_subtotal(self):
        for record in self:
            record.total_subtotal = sum(line.subtotal for line in record.line_ids)
            record.total_current_amount = sum(line.current_level_amount for line in record.line_ids)
            record.total_next_amount = sum(line.next_level_amount for line in record.line_ids)

    def open_project_wizard(self):
        """打开项目视图 批量添加项目"""
        for order in self:
            return {
                'name': '批量选择项目向导',
                'view_mode': 'form',
                'res_model': 'project.selection.wizard',
                'type': 'ir.actions.act_window',
                'target': 'new',
            }


class DuesIncomeExpenditureLine(models.Model):
    _name = 'dues.income.expenditure.line'
    _inherit = ['mail.thread']
    _description = '年度党费收支、结存情况明细表'

    due_id = fields.Many2one(
        'dues.income.expenditure',  # 关联主表模型
        string='关联主表',
        ondelete='cascade',  # 主表记录删除时级联删除明细
        index=True  # 添加索引提升查询性能
    )
    project_ids = fields.Many2many(
        'dues.income.expenditure.items',
        string='关联项目',
        ondelete='cascade'
    )
    type = fields.Selection(related='project_ids.type', string='分类')
    subtotal = fields.Float(string='总计', digits='Amount')
    current_level_amount = fields.Float(string='本级', digits='Amount')
    next_level_amount = fields.Float(string='下一级汇总', digits='Amount')
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        change_default=True,
        default=lambda self: self.env.company)
