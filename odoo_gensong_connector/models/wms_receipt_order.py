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

# 首先构造一个SDK实例
api_sdk = K3CloudApiSdk()
# config_node:配置文件中的节点名称
api_sdk.Init(config_path='rhino-data-nexus/sdk/conf.ini', config_node='config')
# 此处仅构造保存接口的部分字段数据示例，使用时请参考WebAPI具体接口的实际参数列表
current_time = time.strftime('%Y%m%d%H%M%S', time.localtime())


class WmsReceiptOrder(models.Model):
    _inherit = 'wms.receipt.order'

    # =============== 收料/入库侧单据同步 ===============
    # =============== 收料/入库侧单据同步 ===============
    # =============== 收料/入库侧单据同步 ===============
    def action_StockIn_BillQuery(self):
        try:
            self.search_StockIn_BillQuery()    # 查采购入库单
            # self.search_Prd_InStock_BillQuery()  # 查生产入库单
        except Exception as e:
            _logger.error('接口返回结果：{}'.format(e))

    # =============== 采购入库单 ===============
    # =============== 采购入库单 ===============
    # =============== 采购入库单 ===============
    def search_StockIn_BillQuery(self):
        """
        本接口用于查旬业务状态为“审核中”的数据，去驱动WMS去搬运；
        AGV搬运完成后，调用接口将单据状态变更为“C已审核”确认库存
        21 中裕软管科技股份有限公司  库表ID：101124
        23 安徽优耐德管道技术有限公司  库表ID：101127

        "and FDocumentStatus = 'B' " "and FCancelStatus = 'A' "
        :return:
        """
        self.Data_InStock_BillQuery(Limit=100, FilterString="FBILLNO like '%%' "
                                                            "and FDocumentStatus = 'B' " "and FCancelStatus = 'A' "
                                                            "and FSTOCKORGID = '101127'" )

    def Data_InStock_BillQuery(self, **kwargs):
        """
        本接口用于实现采购入库单 (STK_INSTOCK) 的单据查询(json)功能
        :param kwargs:  替换para中参数，示例：FieldKeys=“Fname",Limit=1000
        :return:
        """
        stock_in_obj = self.env['wms.receipt.order']  # 采购入库单
        material_obj = self.env['wms.material.info']
        stock_obj = self.env['wms.stock.info']  # 仓库
        unit_obj = self.env['wms.unit.info']
        para = {
            "FormId": "STK_INSTOCK",
            "FieldKeys": "FBILLNO, FInStockEntry_FSEQ, FInStockEntry_FEntryID, FPOORDERNO, FOBJECTTYPEID, FMATERIALID, FUNITID, FLOT, FLOT_TEXT, FSTOCKID, FMUSTQTY, FREALQTY, FDocumentStatus, FCancelStatus",
            "FilterString": "'FBILLNO'=""",
            "OrderString": "",
            "TopRowCount": 2000,
            "StartRow": 0,
            "Limit": 2000,
            "SubSystemId": ""
        }
        if kwargs:
            para.update(kwargs)
        res = {}
        response = api_sdk.BillQuery(para)
        try:
            res = json.loads(response)
            _logger.info('采购入库单查询接口请求返回: {}'.format(res))
        except Exception as e:
            _logger.error('采购入库单查询接口请求返回错误: {}'.format(e))
        if len(res) > 0:
            for line in res:  # 遍历写入数据
                # 写入采购入库单数据
                material_record = material_obj.search([('MaterialId', '=', line['FMATERIALID'])])
                warehouse_record = stock_obj.search([('StockId', '=', line['FSTOCKID'])])
                unit_record = unit_obj.search([('UnitId', '=', line['FUNITID'])])
                stock_in_record = stock_in_obj.search([('TMBillNo', '=', line['FBILLNO']),
                                                     ('FEntryID', '=', line['FInStockEntry.FEntryID'])])
                pv = {
                    'TMBillNo': line['FBILLNO'],
                    'POOrderNO': line['FPOORDERNO'],
                    'Order': line['FInStockEntry.FSEQ'], # 由于云星空接口限制，取不到行号，用料号去唯一标识行号（同一张单据行料号不能出现重复情况）
                    'FEntryID': line['FInStockEntry.FEntryID'],
                    'BillType': line['FOBJECTTYPEID'],
                    'MaterialId': material_record.id or False,
                    'XCode': material_record.XCode or False,
                    'XName': material_record.XName or False,
                    'Spec': material_record.Spec or False,
                    'Quantity': line['FMUSTQTY'] or False,
                    'UnitId': unit_record.id or False,
                    'UnitCode': unit_record.XCode or False,
                    'UnitName': unit_record.XName or False,
                    'BatchNo': line['FLOT.TEXT'] or False,
                    'CkStockId': False,
                    'CkCode': '000',
                    'CkName': '待转区',
                    'RkStockId': warehouse_record.id or False,
                    'RkCode': warehouse_record.XCode or False,
                    'RkName': warehouse_record.XName or False,
                    'DocumentStatus': line['FDocumentStatus'],
                    'CancelStatus': line['FCancelStatus'],
                    'SyncState': 0,
                }
                if stock_in_record and material_record and stock_in_record.SyncState == 1:
                    continue
                if stock_in_record and material_record and stock_in_record.SyncState == 0:
                    stock_in_record.write(pv)
                elif not stock_in_record and material_record:
                    stock_in_obj.create(pv)

    # =============== 生产入库单 ===============
    # =============== 生产入库单 ===============
    # =============== 生产入库单 ===============
    def search_Prd_InStock_BillQuery(self):
        """
        本接口用于查旬业务状态为“审核中”的数据，去驱动WMS去搬运；
        AGV搬运完成后，调用接口将单据状态变更为“C已审核”确认库存
        21 中裕软管科技股份有限公司  库表ID：101124
        23 安徽优耐德管道技术有限公司  库表ID：101127

        "and FDocumentStatus = 'B' " "and FCancelStatus = 'A' "
        :return:
        """
        self.Data_Prd_InStock_BillQuery(Limit=100, FilterString="FBILLNO like '%%' "
                                                                "and FDocumentStatus = 'B' " "and FCancelStatus = 'A' "
                                                                "and FSTOCKORGID = '101127'" )

    def Data_Prd_InStock_BillQuery(self, **kwargs):
        """
        本接口用于实现生产入库单 (PRD_INSTOCK) 的单据查询(json)功能
        :param kwargs:  替换para中参数，示例：FieldKeys=“Fname",Limit=1000
        :return:
        """
        stock_in_obj = self.env['wms.receipt.order']  # 生产入库单
        material_obj = self.env['wms.material.info']
        stock_obj = self.env['wms.stock.info']  # 仓库
        unit_obj = self.env['wms.unit.info']
        para = {
            "FormId": "PRD_INSTOCK",
            "FieldKeys": "FBILLNO, FEntity_FSEQ, FEntity_FEntryID, FFORMID, FMATERIALID, FUNITID, FLOT, FLOT_TEXT, FWORKSHOPID1, FSTOCKID, FMUSTQTY, FDocumentStatus, FCancelStatus",
            "FilterString": "'FBILLNO'=""",
            "OrderString": "",
            "TopRowCount": 2000,
            "StartRow": 0,
            "Limit": 2000,
            "SubSystemId": ""
        }
        if kwargs:
            para.update(kwargs)
        res = {}
        response = api_sdk.BillQuery(para)
        try:
            res = json.loads(response)
            # _logger.info('生产入库单查询接口请求返回: {}'.format(res))
        except Exception as e:
            _logger.error('生产入库单查询接口请求返回错误: {}'.format(e))
        if len(res) > 0:
            for line in res:  # 遍历写入数据
                # 写入生产入库单数据
                material_record = material_obj.search([('MaterialId', '=', line['FMATERIALID'])])
                workshop_record = stock_obj.search([('StockId', '=', line['FWORKSHOPID1'])])
                stock_record = stock_obj.search([('StockId', '=', line['FSTOCKID'])])
                unit_record = unit_obj.search([('UnitId', '=', line['FUNITID'])])
                stock_in_record = stock_in_obj.search([('TMBillNo', '=', line['FBILLNO']),
                                                     ('FEntryID', '=', line['FEntity.FEntryID'])])
                pv = {
                    'TMBillNo': line['FBILLNO'],
                    'Order': line['FEntity.FSEQ'], # 由于云星空接口限制，取不到行号，用料号去唯一标识行号（同一张单据行料号不能出现重复情况）
                    'FEntryID': line['FEntity.FEntryID'],
                    'BillType': line['FFORMID'],
                    'MaterialId': material_record.id or False,
                    'XCode': material_record.XCode or False,
                    'XName': material_record.XName or False,
                    'Spec': material_record.Spec or False,
                    'Quantity': line['FMUSTQTY'] or False,
                    'UnitId': unit_record.id or False,
                    'UnitCode': unit_record.XCode or False,
                    'UnitName': unit_record.XName or False,
                    'BatchNo': line['FLOT.TEXT'] or False,
                    'CkStockId': workshop_record.id or False,   # 车间出
                    'CkCode': workshop_record.XCode or False,
                    'CkName': workshop_record.XName or False,
                    'RkStockId': stock_record.id or False,  # 仓库入
                    'RkCode': stock_record.XCode or False,
                    'RkName': stock_record.XName or False,
                    'DocumentStatus': line['FDocumentStatus'],
                    'CancelStatus': line['FCancelStatus'],
                    'SyncState': 0,
                }
                if stock_in_record and material_record and stock_in_record.SyncState == 1:
                    continue
                if stock_in_record and material_record and stock_in_record.SyncState == 0:
                    stock_in_record.write(pv)
                elif not stock_in_record and material_record:
                    stock_in_obj.create(pv)
