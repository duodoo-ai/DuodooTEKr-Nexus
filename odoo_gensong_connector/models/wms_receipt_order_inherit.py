# -*- coding: utf-8 -*-
"""
@Time    : 2024/12/05 8:20
@Author  : Jason Zou
@Email   : zou.jason@qq.com
@mobile  : 18951631470
"""
import json, time, logging
from datetime import datetime
from odoo import api, fields, models
from k3cloud_webapi_sdk.main import K3CloudApiSdk
_logger = logging.getLogger(__name__)

# 首先构造一个SDK实例
api_sdk = K3CloudApiSdk()
# config_node:配置文件中的节点名称
api_sdk.Init(config_path='duodoo-ai/rhino-data-nexus/sdk/conf.ini', config_node='config')
# 此处仅构造保存接口的部分字段数据示例，使用时请参考WebAPI具体接口的实际参数列表
current_time = time.strftime('%Y%m%d%H%M%S', time.localtime())


class WmsReceiptOrder(models.Model):
    _inherit = 'wms.receipt.order'

    # =============== 生产订单侧单据同步 ===============
    # =============== 生产订单侧单据同步 ===============
    # =============== 生产订单侧单据同步 ===============
    def action_Prd_Mo_BillQuery(self):
        try:
            self.search_Prd_Mo_BillQuery()    # 查生产订单
        except Exception as e:
            _logger.error('接口返回结果：{}'.format(e))

    # =============== 查生产订单 ===============
    # =============== 查生产订单 ===============
    # =============== 查生产订单 ===============
    def search_Prd_Mo_BillQuery(self):
        """
        本接口用于查旬业务状态为“审核中”的数据，去驱动WMS去搬运；
        AGV搬运完成后，调用接口将单据状态变更为“C已审核”确认库存
        21 中裕软管科技股份有限公司  库表ID：101124
        23 安徽优耐德管道技术有限公司  库表ID：101127

        "and FDocumentStatus = 'B' " "and FCancelStatus = 'A' "
        :return:
        """
        self.Data_Prd_Mo_BillQuery(Limit=100, FilterString="FBILLNO like '%%' "                                                           
                                                           "and FCancelStatus = 'A' "
                                                           "and FPRDORGID = '101127'"
                                   )

    def Data_Prd_Mo_BillQuery(self, **kwargs):
        """
        本接口用于实现从生产订单 去驱动半成品入库 (STK_INSTOCK) 的单据查询(json)功能
        :param kwargs:  替换para中参数，示例：FieldKeys=“Fname",Limit=1000

        同步的要有生产订单号  生产订单行号，需求单据 ，需求单据行号 、物料编码、零件号、物料名称、生产数量、规格型号，生产单位、生产车间
        显示的话需求单据号、需求单据行号、物料、 零件号、规格型号，数量、单位
        :return:
        """
        stock_in_obj = self.env['wms.receipt.order']  # 采购入库单
        material_obj = self.env['wms.material.info']
        stock_obj = self.env['wms.stock.info']  # 仓库
        unit_obj = self.env['wms.unit.info']
        para = {
            "FormId": "PRD_MO",
            "FieldKeys": "FBILLNO, FFORMID, FMATERIALID,  FBASEUNITID, FQTY, FWORKSHOPID, FDATE, FDocumentStatus, FCancelStatus",
            "FilterString": "'FBILLNO'=""",
            "OrderString": "FDATE DESC",
            "TopRowCount": 10,
            "StartRow": 0,
            "Limit": 10,
            "SubSystemId": ""
        }
        if kwargs:
            para.update(kwargs)
        res = {}
        response = api_sdk.BillQuery(para)
        try:
            res = json.loads(response)
            _logger.info('生产订单查询接口请求返回: {}'.format(res))
        except Exception as e:
            _logger.error('生产订单查询接口请求返回错误: {}'.format(e))
        # print(res)
        if len(res) > 0:
            for line in res:  # 遍历写入数据
                # 写入采购入库单数据
                material_record = material_obj.search([('MaterialId', '=', line['FMATERIALID'])])
                warehouse_record = stock_obj.search([('StockId', '=', line['FWORKSHOPID'])])
                unit_record = unit_obj.search([('UnitId', '=', line['FBASEUNITID'])])
                stock_in_record = stock_in_obj.search([('TMBillNo', '=', line['FBILLNO']),
                                                     ('Order', '=', line['FMATERIALID'])])
                pv = {
                    'TMBillNo': line['FBILLNO'],
                    'POOrderNO': False,
                    'Order': line['FMATERIALID'], # 由于云星空接口限制，取不到行号，用料号去唯一标识行号（同一张单据行料号不能出现重复情况）
                    'BillType': line['FFORMID'],
                    'MaterialId': material_record.id or False,
                    'XCode': material_record.XCode or False,
                    'XName': material_record.XName or False,
                    'Spec': material_record.Spec or False,
                    'Quantity': line['FQTY'] or False,
                    'UnitId': unit_record.id or False,
                    'UnitCode': unit_record.XCode or False,
                    'UnitName': unit_record.XName or False,
                    'BatchNo': False,
                    'CkStockId': warehouse_record.id or False,
                    'CkCode': warehouse_record.XCode or False,
                    'CkName': warehouse_record.XName or False,
                    'RkStockId': False,
                    'RkCode': False,
                    'RkName': False,
                    'DocumentStatus': line['FDocumentStatus'],
                    'CancelStatus': line['FCancelStatus'],
                    'SyncState': 0,
                    'SyncTime': datetime.strptime(line['FDATE'], '%Y-%m-%dT%H:%M:%S'),
                }
                if stock_in_record and material_record and stock_in_record.SyncState == 1:
                    continue
                if stock_in_record and material_record and stock_in_record.SyncState == 0:
                    stock_in_record.write(pv)
                elif not stock_in_record and material_record:
                    stock_in_obj.create(pv)

