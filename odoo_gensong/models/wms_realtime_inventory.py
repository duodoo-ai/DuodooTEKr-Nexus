# -*- coding: utf-8 -*-
"""
@Time    : 2024/12/05 8:20
@Author  : Jason Zou
@Email   : zou.jason@qq.com
@mobile  : 18951631470
"""
import json, time, logging
from string import digits

from odoo import api, fields, models
from k3cloud_webapi_sdk.main import K3CloudApiSdk
_logger = logging.getLogger(__name__)


class WmsRealtimeInventory(models.Model):
    _name = 'wms.realtime.inventory'
    _description = '实时库存视图'

    # WMS扫码实时查询上位系统上位绑定的物料信息
    FID = fields.Char(string='唯一ID', help='上位系统写入，不可为空')
    BillType = fields.Char(string='单据类型', help='上位系统写入，不可为空')
    StockOrgId = fields.Char(string='库存组织ID', help='上位系统写入，不可为空')
    StockId = fields.Many2one('wms.stock.info', string='仓库ID', help='上位系统写入，不可为空')
    StockCode = fields.Char(related='StockId.XCode', string='仓库编码', help='上位系统写入，不可为空')
    StockName = fields.Char(related='StockId.XName', string='仓库名称')
    MaterialId = fields.Many2one('wms.material.info', string='物料代码', help='上位系统写入，不可为空')
    MaterialCode = fields.Char(related='MaterialId.XCode', string='物料代码', help='上位系统写入，不可为空')
    MaterialName = fields.Char(related='MaterialId.XName', string='物料名称', help='上位系统写入，不可为空')
    Spec = fields.Char(string='规格型号', help='上位系统写入，不可为空')
    BatchNo = fields.Char(string='批次', help='上位系统写入，不可为空')
    UnitId = fields.Many2one('wms.unit.info', string='基础单位ID', help='上位系统写入，不可为空')
    UnitCode = fields.Char(related='UnitId.XCode', string='单位编码', help='上位系统写入，不可为空')
    UnitName = fields.Char(related='UnitId.XName', string='基础单位', help='上位系统写入，不可为空')
    BaseQty = fields.Float(string='在库数量', digits=(23,6), help='上位系统写入，不可为空')
    BaseLockQty = fields.Float(string='锁库数量', digits=(23,6), help='上位系统写入，不可为空')
    SyncState = fields.Integer(string='同步状态', default=0, help='0：上位系统写入；1：WMS已同步')
    SyncTime = fields.Datetime(string='入库日期', help='WMS写入')
    company_id = fields.Many2one(
        'res.company',
        string='公司',
        change_default=True,
        default=lambda self: self.env.company)
