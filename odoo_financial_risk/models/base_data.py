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

class BaseContractCategory(models.Model):
    _name = 'base.contract.category'
    _description = '合同分类及名称'

    name = fields.Char(string="合同分类及名称", required=True)
    code = fields.Char(string='合同编号')
    active = fields.Boolean(string="启用", default=True)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        change_default=True,
        default=lambda self: self.env.company)


class BaseContractOrganizer(models.Model):
    _name = 'base.contract.organizer'
    _description = '合同承办单位'

    name = fields.Char(string="合同承办单位", required=True)
    code = fields.Char(string='编号')
    active = fields.Boolean(string="启用", default=True)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        change_default=True,
        default=lambda self: self.env.company)


class BaseContractOpposing(models.Model):
    _name = 'base.contract.opposing'
    _description = '对方单位名称'

    name = fields.Char(string="对方单位名称", required=True)
    code = fields.Char(string='编号')
    active = fields.Boolean(string="启用", default=True)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        change_default=True,
        default=lambda self: self.env.company)


class BaseTechnicalCommittees(models.Model):
    _name = 'base.technical.committees'
    _description = '归口单位'

    name = fields.Char(string="归口单位名称", required=True)
    code = fields.Char(string='编号')
    active = fields.Boolean(string="启用", default=True)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        change_default=True,
        default=lambda self: self.env.company)


class BaseEntrustedCommittees(models.Model):
    _name = 'base.entrusted.committees'
    _description = '受托单位名称'

    name = fields.Char(string="受托单位名称", required=True)
    code = fields.Char(string='编号')
    active = fields.Boolean(string="启用", default=True)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        change_default=True,
        default=lambda self: self.env.company)

class VoucherType(models.Model):
    _name = 'voucher.type'
    _description = '凭证类型'

    name = fields.Char(string="凭证类型", required=True)
    code = fields.Char(string='编号')
    active = fields.Boolean(string="启用", default=True)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        change_default=True,
        default=lambda self: self.env.company)

class ProjectResponsibilityDepartment(models.Model):
    _name = 'project.responsibility.department'
    _description = '项目责任部门'

    name = fields.Char(string="项目责任部门", required=True)
    code = fields.Char(string='编号')
    active = fields.Boolean(string="启用", default=True)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        change_default=True,
        default=lambda self: self.env.company)

class ProjectCategory(models.Model):
    _name = 'project.category'
    _description = '项目分类'

    name = fields.Char(string="项目大类", required=True)
    code = fields.Char(string='编号')
    note = fields.Char(string='填报说明')
    active = fields.Boolean(string="启用", default=True)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        change_default=True,
        default=lambda self: self.env.company)

class SubjectComparison(models.Model):
    _name = 'subject.comparison'
    _description = '科目对照表'

    name = fields.Char(string="记账会计科目描述", required=True)
    code = fields.Char(string='记账会计科目编码')
    active = fields.Boolean(string="启用", default=True)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        change_default=True,
        default=lambda self: self.env.company)

class NatureAccountsPayable(models.Model):
    _name = 'nature.accounts.payable'
    _description = '往来款项性质'

    name = fields.Char(string="往来款项性质名称", required=True)
    code = fields.Char(string='往来款项性质编码')
    active = fields.Boolean(string="启用", default=True)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        change_default=True,
        default=lambda self: self.env.company)

class NatureReason(models.Model):
    _name = 'nature.reason'
    _description = '原因'

    name = fields.Char(string="原因", required=True)
    code = fields.Char(string='原因编码')
    active = fields.Boolean(string="启用", default=True)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        change_default=True,
        default=lambda self: self.env.company)

class DuesIncomeExpenditureItems(models.Model):
    _name = 'dues.income.expenditure.items'
    _description = '党费收支项目'

    name = fields.Char(string="收支项目", required=True, index=True)
    code = fields.Char(string='项目编码')
    type = fields.Selection([
        ('收入', '收入'),
        ('支出', '支出'),
        ('使用', '使用'),
    ], string='分类')
    active = fields.Boolean(string="启用", default=True)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        change_default=True,
        default=lambda self: self.env.company)

class AccountBusinessTravelItems(models.Model):
    _name = 'account.business.travel.items'
    _description = '商旅指标项目'

    name = fields.Char(string="指标项目", required=True, index=True)
    code = fields.Char(string='项目编码')
    active = fields.Boolean(string="启用", default=True)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        change_default=True,
        default=lambda self: self.env.company)

