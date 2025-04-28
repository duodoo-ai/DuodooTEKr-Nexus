# -*- coding: utf-8 -*-
"""
@Time    : 2025/1/6 8:20
@Author  : Jason Zou
@Email   : zou.jason@qq.com
@mobile  : 18951631470
"""
import json, time, logging
from odoo import api, fields, models
from k3cloud_webapi_sdk.main import K3CloudApiSdk
_logger = logging.getLogger(__name__)

current_time = time.strftime('%Y%m%d%H%M%S', time.localtime())


class QstamperCategory(models.Model):
    _name = 'qstamper.category'
    _description = '印章类型'

    name = fields.Char(string='名称', help='印章类型名称，唯一性')
    active = fields.Boolean(string='状态', default=True, help='True：默认创建；False：归档，不可使用')
    company_id = fields.Many2one(
        'res.company',
        string='公司',
        change_default=True,
        default=lambda self: self.env.company)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', '印章类型不能重名')
    ]


class QstamperEquipment(models.Model):
    _name = 'qstamper.equipment'
    _description = '印章设备列表'
    # YXYG04_01
    name = fields.Char(string='名称', help='印章名称，唯一性')
    uuid = fields.Char(string='唯一标识符', help='唯一标识符，全局唯一性')
    tenant = fields.Char(string='租户标识', help='租户标识，全局唯一性')
    deptName = fields.Char(string='部门名称', help='部门名称')
    location = fields.Char(string='位置', help='位置')
    type = fields.Char(string='类型', help='类型')
    online = fields.Boolean(string='启用', default=True, help='在线状态')
    company_id = fields.Many2one(
        'res.company',
        string='公司',
        change_default=True,
        default=lambda self: self.env.company)

    _sql_constraints = [
        ('uuid_uniq', 'unique(uuid)', '印章唯一标识')
    ]


class QstamperFileType(models.Model):
    _name = 'qstamper.file.type'
    _description = '申请类型'
    # YXYG03_05
    name = fields.Char(string='名称', help='印章名称，唯一性')
    fileid = fields.Char(string='文件类型ID', help='唯一标识符，全局唯一性')
    tenant = fields.Char(string='租户标识', help='租户标识，全局唯一性')
    online = fields.Boolean(string='启用', default=True, help='在线状态')
    company_id = fields.Many2one(
        'res.company',
        string='公司',
        change_default=True,
        default=lambda self: self.env.company)

    _sql_constraints = [
        ('fileid_uniq', 'unique(fileid)', '文件类型唯一标识')
    ]



class QstamperApproval(models.Model):
    _name = 'qstamper.approval'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = '云玺印管平台'

    name = fields.Char(string='订单号', help='采购订单号或销售订单号，唯一性')
    BillType = fields.Char(string='单据类型', help='上位系统写入，不可为空，唯一性')
    applicant = fields.Char(string='申请人', help='上位系统写入，不可为空，唯一性')
    category = fields.Many2one('qstamper.category', string='印章名称', help='印章类型名称')
    date = fields.Date(string='单据日期', help='上位系统写入，不可为空')
    SyncState = fields.Boolean(string='已授权', default=False, help='False：创建默认；True：云玺印管平台已处理')
    ControlState = fields.Boolean(string='已受控', default=False, help='False：创建默认；True：加受控图变更为True状态')
    SyncCode = fields.Char(string='授权码', help='云玺印管平台返回申请授权码')
    DocumentStatus = fields.Char(string='数据状态', help='上位系统写入，不可为空')
    CancelStatus = fields.Char(string='禁用状态', help='上位系统写入，不可为空')
    # 附件
    attachment_id = fields.Char(string='附件ID(InterId)', help='记录云星空单据唯一FID（InterId）')
    FileSize = fields.Char(string='文件大小', help='文件大小')
    source_binary_data = fields.Binary(
        "源附件文件", help="k3-源附件文件", default=False, attachment=True, copy=False
    )
    source_binary_data_name = fields.Char("源附件文件名", copy=False)
    dest_attach_data = fields.Binary("受控件附件", readonly=False, copy=False)
    dest_binary_data_name = fields.Char("受控件附件文件名", copy=False)
    company_id = fields.Many2one(
        'res.company',
        string='公司',
        change_default=True,
        default=lambda self: self.env.company)
