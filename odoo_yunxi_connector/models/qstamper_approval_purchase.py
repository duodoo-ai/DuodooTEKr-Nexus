# -*- coding: utf-8 -*-
"""
@Time    : 2025/1/6 8:20
@Author  : Jason Zou
@Email   : zou.jason@qq.com
@mobile  : 18951631470
"""
import json, time, logging
import base64
from odoo import api, fields, models
from k3cloud_webapi_sdk.main import K3CloudApiSdk
_logger = logging.getLogger(__name__)

# 首先构造一个SDK实例
api_sdk = K3CloudApiSdk()
# config_node:配置文件中的节点名称
api_sdk.Init(config_path='tone_good/sdk/conf.ini', config_node='config')
# 此处仅构造保存接口的部分字段数据示例，使用时请参考WebAPI具体接口的实际参数列表
current_time = time.strftime('%Y%m%d%H%M%S', time.localtime())


class QstamperApproval(models.Model):
    _inherit = 'qstamper.approval'

    # =============== 从ERP查询订单数据 到中间平台 待审批 ===============
    # =============== 从ERP查询订单数据 到中间平台 待审批 ===============
    # =============== 从ERP查询订单数据 到中间平台 待审批 ===============
    def Action_Purchase_BillQuery(self):
        """
        本接口用于实现的单据查询(json)功能
        :param kwargs:  替换para中参数，示例：FieldKeys=“Fname",Limit=1000
        :return:

        "and FDocumentStatus = 'C' "
        """
        try:
            self.Search_PurchaseOrder_BillQuery(Limit=10,
                                    FilterString="FBILLNO like '%%' "
                                                 "and FDocumentStatus = 'C' "
                                                 "and FCancelStatus = 'A' ")  # 查采购订单
        except Exception as e:
            _logger.error('云玺印管：采购订单推送云玺印管平台获得授权码接口错误：{}'.format(e))

    # =============== 采购订单 走云玺印管 平台审批 ===============
    # =============== 采购订单 走云玺印管 平台审批 ===============
    # =============== 采购订单 走云玺印管 平台审批 ===============
    def Search_PurchaseOrder_BillQuery(self, **kwargs):
        """
        本接口用于实现采购订单(PUR_PurchaseOrder) 的单据查询(json)功能
        :param kwargs:  替换para中参数，示例：FieldKeys=“Fname",Limit=1000
        :return:
        """
        approval_obj = self.env['qstamper.approval']
        para = {
            "FormId": "PUR_PurchaseOrder",
            "FieldKeys": "FBILLNO, FOBJECTTYPEID, FPURCHASERID, FDATE, FDOCUMENTSTATUS, FCANCELSTATUS",
            "FilterString": "'FNumber'=""",
            "OrderString": "FDATE DESC",
            "TopRowCount": 1000,
            "StartRow": 0,
            "Limit": 1000,
            "SubSystemId": ""
        }
        if kwargs:
            para.update(kwargs)
        response = api_sdk.BillQuery(para)
        res = {}
        try:
            res = json.loads(response)
            # _logger.error('云玺印管：销售订单请求云星空单据查询接口结果: {}'.format(res))
        except Exception as e:
            _logger.error('云玺印管：销售订单请求云星空单据查询接口错误: {}'.format(e))
        tot_len = int(len(res) / 100 + 1)
        start = 0
        end = 100
        if len(res) > 0:
            for ci in range(0, tot_len):
                records2 = res[start:end]
                if not records2:
                    continue
                for line in records2:  # 遍历写入数据
                    # 写入数据
                    approval_record = approval_obj.search([('name', '=', line['FBILLNO'])])
                    pv = {
                        'name': line['FBILLNO'],
                        'BillType': line['FOBJECTTYPEID'],
                        'applicant': line['FPURCHASERID'],
                        'category': False,
                        'date': line['FDATE'],
                        'SyncState': False,
                        'DocumentStatus': line['FDOCUMENTSTATUS'],
                        'CancelStatus': line['FCANCELSTATUS'],
                    }
                    if approval_record and approval_record.SyncState:
                        continue
                    if approval_record and not approval_record.SyncState:
                        approval_record.write(pv)
                    elif not approval_record:
                        approval_obj.create(pv)
                start = end
                end = end + 100