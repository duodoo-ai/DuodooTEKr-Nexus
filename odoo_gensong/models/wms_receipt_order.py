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


class WmsReceiptOrder(models.Model):
    _name = 'wms.receipt.order'
    _description = '入库库前收货/入库完成反馈'

    # WMS扫码实时查询上位系统绑定的单据信息
    TMBillNo = fields.Char(string='单号', help='上位系统写入，不可为空。对应单号。')
    POOrderNO = fields.Char(string='订单单号', help='上位系统写入，不可为空。对应采购订单单号。')
    Order = fields.Char(string='行号', help='上位系统写入，不可为空。对应单据明细行。')
    FEntryID = fields.Char(string='分录ID', help='上位系统写入，不可为空。对应单据明细行 分录ID。')
    BillType = fields.Char(string='单据类型', help='上位系统写入，不可为空')
    MaterialId = fields.Many2one('wms.material.info', string='物料ID', help='上位系统写入，不可为空')
    XCode = fields.Char(related='MaterialId.XCode', string='物料代码', help='上位系统写入，不可为空')
    XName = fields.Char(related='MaterialId.XName', string='物料名称', help='上位系统写入，不可为空')
    Spec = fields.Char(related='MaterialId.Spec', string='规格型号', help='上位系统写入')
    Quantity = fields.Char(string='计划数量', help='上位系统写入，不可为空')
    UnitId = fields.Many2one('wms.unit.info', string='基础单位ID', help='上位系统写入，不可为空')
    UnitCode = fields.Char(related='UnitId.XCode', string='单位编码', help='上位系统写入，不可为空')
    UnitName = fields.Char(related='UnitId.XName', string='基础单位', help='上位系统写入，不可为空')
    BatchNo = fields.Char(string='批次', help='上位系统写入')
    CkStockId = fields.Many2one('wms.stock.info', string='调出仓库ID', help='上位系统写入')
    CkCode = fields.Char(related='CkStockId.XCode', string='调出仓库编码', help='上位系统写入')
    CkName = fields.Char(related='CkStockId.XName', string='调出仓库名称', help='上位系统写入')
    RkStockId = fields.Many2one('wms.stock.info', string='调入仓库ID', help='上位系统写入')
    RkCode = fields.Char(related='RkStockId.XCode', string='调入仓库编码', help='上位系统写入')
    RkName = fields.Char(related='RkStockId.XName', string='调入仓库名称', help='上位系统写入')
    DocumentStatus = fields.Char(string='单据状态', help='业务状态。上位系统写入，不可为空(标识单据启停进度)')
    CancelStatus = fields.Char(string='禁用状态', help='作废状态。上位系统写入，不可为空(标识物料启停状态)')
    # WMS扫码驱动AGV执行并返回执行数据
    ActualQty = fields.Char(string='执行数量', help='WMS写入')
    Area = fields.Char(string='物料分区', help='WMS写入')
    TaskId = fields.Char(string='任务Id', help='WMS写入')
    SyncState = fields.Integer(string='同步状态', default=0, help='0：上位系统写入；1：WMS已同步')
    SyncTime = fields.Datetime(string='同步时间', help='WMS写入')
    company_id = fields.Many2one(
        'res.company',
        string='公司',
        change_default=True,
        default=lambda self: self.env.company)
