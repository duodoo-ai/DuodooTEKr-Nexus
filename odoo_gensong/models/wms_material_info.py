# -*- coding: utf-8 -*-
"""
@Time    : 2024/12/05 8:20
@Author  : Jason Zou
@Email   : zou.jason@qq.com
@mobile  : 18951631470
"""
import json, time, logging
from odoo import api, fields, models
from k3cloud_webapi_sdk.main import K3CloudApiSdk
_logger = logging.getLogger(__name__)


class WmsStockInfo(models.Model):
    _name = 'wms.stock.info'
    _description = '仓库'

    # 上位系统增量同步数据至中间表，WMS读取
    StockId = fields.Char(string='仓库内码', help='上位系统写入，不可为空，唯一性')
    XCode = fields.Char(string='编码', help='上位系统写入，不可为空，唯一性')
    XName = fields.Char(string='名称', help='上位系统写入，不可为空')
    Spec = fields.Selection([('车间', '车间'), ('仓库', '仓库')], string='类型', help='上位系统写入，不可为空')
    DocumentStatus = fields.Char(string='数据状态', help='上位系统写入，不可为空')
    ForbidStatus = fields.Char(string='禁用状态', help='上位系统写入，不可为空')
    company_id = fields.Many2one(
        'res.company',
        string='公司',
        change_default=True,
        default=lambda self: self.env.company)

class WmsUnitInfo(models.Model):
    _name = 'wms.unit.info'
    _description = '计量单位'

    # 上位系统增量同步数据至中间表，WMS读取
    UnitId = fields.Char(string='物料内码', help='上位系统写入，不可为空，唯一性')
    XCode = fields.Char(string='编码', help='上位系统写入，不可为空，唯一性')
    XName = fields.Char(string='名称', help='上位系统写入，不可为空')
    DocumentStatus = fields.Char(string='数据状态', help='上位系统写入，不可为空')
    ForbidStatus = fields.Char(string='禁用状态', help='上位系统写入，不可为空')
    company_id = fields.Many2one(
        'res.company',
        string='公司',
        change_default=True,
        default=lambda self: self.env.company)


class WmsCategoryInfo(models.Model):
    _name = 'wms.category.info'
    _description = '物料类别'

    # 上位系统增量同步数据至中间表，WMS读取
    CategoryId = fields.Char(string='物料内码', help='上位系统写入，不可为空，唯一性')
    XCode = fields.Char(string='编码', help='上位系统写入，不可为空，唯一性')
    XName = fields.Char(string='名称', help='上位系统写入，不可为空')
    DocumentStatus = fields.Char(string='数据状态', help='上位系统写入，不可为空')
    ForbidStatus = fields.Char(string='禁用状态', help='上位系统写入，不可为空')
    company_id = fields.Many2one(
        'res.company',
        string='公司',
        change_default=True,
        default=lambda self: self.env.company)


class WmsMaterialInfo(models.Model):
    _name = 'wms.material.info'
    _description = '基础物料同步中间表'

    # 上位系统增量同步物料数据至中间表，WMS读取
    UseOrgID = fields.Char(string='使用组织', help='上位系统写入，不可为空，唯一性')
    MaterialId = fields.Char(string='物料内码', help='上位系统写入，不可为空，唯一性')
    XCode = fields.Char(string='物料代码', help='上位系统写入，不可为空，唯一性')
    XName = fields.Char(string='物料名称', help='上位系统写入，不可为空')
    Spec = fields.Char(string='规格型号', help='上位系统写入')
    Class = fields.Many2one('wms.category.info', string='分类', help='上位系统写入')
    Class_name = fields.Char(related='Class.XName', string='物料分类', help='上位系统写入')
    SmallestUnit = fields.Many2one('wms.unit.info', string='单位', help='上位系统写入，不可为空')
    Unit_name = fields.Char(related='SmallestUnit.XName', string='基础单位', help='上位系统写入，不可为空')
    Upper = fields.Float(string='库存上限', digits=(18, 2), help='上位系统写入')
    Lower = fields.Float(string='库存下限', digits=(18, 2), help='上位系统写入')
    Days = fields.Integer(string='预警天数', default=0, help='上位系统写入')
    DocumentStatus = fields.Char(string='数据状态', help='上位系统写入，不可为空(标识物料启停状态)')
    ForbidStatus = fields.Char(string='禁用状态', help='上位系统写入，不可为空(标识物料启停状态)')

    SyncState = fields.Integer(string='同步状态', default=0, help='0：上位系统写入；1：WMS已同步')
    SyncTime = fields.Datetime(string='同步时间', help='WMS写入')
    company_id = fields.Many2one(
        'res.company',
        string='公司',
        change_default=True,
        default=lambda self: self.env.company)
