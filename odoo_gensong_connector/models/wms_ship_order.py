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
api_sdk.Init(config_path='duodoo-ai/rhino-data-nexus/sdk/conf.ini', config_node='config')
# 此处仅构造保存接口的部分字段数据示例，使用时请参考WebAPI具体接口的实际参数列表
current_time = time.strftime('%Y%m%d%H%M%S', time.localtime())


class WmsShipOrder(models.Model):
    _inherit = 'wms.ship.order'

    # =============== 发料/发货侧单据同步 ===============
    # =============== 发料/发货侧单据同步 ===============
    # =============== 发料/发货侧单据同步 ===============
    def action_StockOut_BillQuery(self):
        try:
            self.Search_STK_TransferDirect_BillQuery()    # 查直接调拨单
            self.Search_PRD_PickMtrl_BillQuery()  # 查生产领料单
            # self.Search_SP_PickMtrl_BillQuery()     # 简单生产领料单
            # self.Search_Stk_MisDelivery_BillQuery()     # 其他出库单
        except Exception as e:
            _logger.error('接口返回结果：{}'.format(e))

    # =============== 直接调拨单 ===============
    # =============== 直接调拨单 ===============
    # =============== 直接调拨单 ===============
    def Search_STK_TransferDirect_BillQuery(self):
        """
        本接口用于查旬业务状态为“审核中”的数据，去驱动WMS去搬运；
        AGV搬运完成后，调用接口将单据状态变更为“C已审核”确认库存
        21 中裕软管科技股份有限公司  库表ID：101124
        23 安徽优耐德管道技术有限公司  库表ID：101127
        "and FDOCUMENTSTATUS = 'B' "
        "and FCANCELSTATUS = 'A' "
        :return:
        """
        self.Data_STK_TransferDirect_BillQuery(Limit=100, FilterString="FBILLNO like '%%'"
                                                                    "and FTRANSFERBIZTYPE = 'InnerOrgTransfer'"
                                                                    "and FDocumentStatus = 'B' " "and FCancelStatus = 'A' "
                                                                    "and FSTOCKORGID = '101127'" )

    def Data_STK_TransferDirect_BillQuery(self, **kwargs):
        """
        本接口用于实现直接调拨单 (STK_STKTRANSFERIN) 的单据查询(json)功能
        :param kwargs:  替换para中参数，示例：FieldKeys=“Fname",Limit=1000
        :return:
        """
        stock_out_obj = self.env['wms.ship.order']  # 直接调拨单
        material_obj = self.env['wms.material.info']
        stock_obj = self.env['wms.stock.info']  # 仓库
        unit_obj = self.env['wms.unit.info']
        para = {
            "FormId": "STK_TransferDirect",
            "FieldKeys": "FBILLNO, FOBJECTTYPEID, FMATERIALID, FUNITID, FSrcStockID, FDestStockID, FQty, FLOT, FLOT_TEXT, FDOCUMENTSTATUS, FCANCELSTATUS",
            "FilterString": "'FBILLNO'=""",
            "OrderString": "",
            "TopRowCount": 1000,
            "StartRow": 0,
            "Limit": 1000,
            "SubSystemId": ""
        }
        if kwargs:
            para.update(kwargs)
        res = {}
        response = api_sdk.BillQuery(para)
        try:
            res = json.loads(response)
            _logger.info('直接调拨单查询接口请求返回: {}'.format(res))
        except Exception as e:
            _logger.error('直接调拨单查询接口请求返回错误: {}'.format(e))
        if len(res) > 0:
            for line in res:  # 遍历写入数据
                # 写入直接调拨单数据
                material_record = material_obj.search([('MaterialId', '=', line['FMATERIALID'])])
                SrcStockID = stock_obj.search([('StockId', '=', line['FSrcStockID'])])
                DestStockID = stock_obj.search([('StockId', '=', line['FDestStockID'])])
                unit_record = unit_obj.search([('UnitId', '=', line['FUNITID'])])
                stock_out_record = stock_out_obj.search([('TMBillNo', '=', line['FBILLNO']),
                                                         ('Order', '=', line['FMATERIALID'])])
                pv = {
                    'TMBillNo': line['FBILLNO'],
                    'Order': line['FMATERIALID'], # 由于云星空接口限制，取不到行号，用料号去唯一标识行号（同一张单据行料号不能出现重复情况）
                    'BillType': line['FOBJECTTYPEID'],
                    'MaterialId': material_record.id or False,
                    'XCode': material_record.XCode or False,
                    'XName': material_record.XName or False,
                    'Spec': material_record.Spec or False,
                    'Quantity': line['FQty'] or False,
                    'UnitId': unit_record.id or False,
                    'UnitCode': unit_record.XCode or False,
                    'UnitName': unit_record.XName or False,
                    'BatchNo': line['FLOT.TEXT'] or False,
                    'CkStockId': SrcStockID.id or False,   # 调出仓库
                    'CkCode': SrcStockID.XCode or False,
                    'CkName': SrcStockID.XName or False,
                    'RkStockId': DestStockID.id or False,   # 调入仓库
                    'RkCode': DestStockID.XCode or False,
                    'RkName': DestStockID.id or False,
                    'DocumentStatus': line['FDOCUMENTSTATUS'],
                    'CancelStatus': line['FCANCELSTATUS'],
                    'SyncState': 0,
                }
                if stock_out_record and material_record and stock_out_record.SyncState == 1:
                    continue
                if stock_out_record and material_record and stock_out_record.SyncState == 0:
                    stock_out_record.write(pv)
                elif not stock_out_record and material_record:
                    stock_out_obj.create(pv)


    # =============== 生产领料单 ===============
    # =============== 生产领料单 ===============
    # =============== 生产领料单 ===============
    def Search_PRD_PickMtrl_BillQuery(self):
        """
        本接口用于查旬业务状态为“审核中”的数据，去驱动WMS去搬运；
        AGV搬运完成后，调用接口将单据状态变更为“C已审核”确认库存
        21 中裕软管科技股份有限公司  库表ID：101124
        23 安徽优耐德管道技术有限公司  库表ID：101127
        "and FDOCUMENTSTATUS = 'B' "
        "and FCANCELSTATUS = 'A' "
        :return:
        """
        self.Data_PRD_PickMtrl_BillQuery(Limit=100, FilterString="FBILLNO like '%%' "
                                                                 "and FDocumentStatus = 'B' " "and FCancelStatus = 'A' "
                                                                 "and FSTOCKORGID = '101127'" )

    def Data_PRD_PickMtrl_BillQuery(self, **kwargs):
        """
        本接口用于实现生产领料单 (PRD_PickMtrl) 的单据查询(json)功能
        :param kwargs:  替换para中参数，示例：FieldKeys=“Fname",Limit=1000
        :return:
        """
        stock_out_obj = self.env['wms.ship.order']  # 生产领料单
        material_obj = self.env['wms.material.info']
        stock_obj = self.env['wms.stock.info']  # 仓库
        unit_obj = self.env['wms.unit.info']
        para = {
            "FormId": "PRD_PickMtrl",
            "FieldKeys": "FBILLNO, FFORMID, FMATERIALID, FUNITID, FSTOCKID, FENTRYWORKSHOPID, FACTUALQTY, FLOT, FLOT_TEXT, FDOCUMENTSTATUS, FCANCELSTATUS",
            "FilterString": "'FBILLNO'=""",
            "OrderString": "",
            "TopRowCount": 1000,
            "StartRow": 0,
            "Limit": 1000,
            "SubSystemId": ""
        }
        if kwargs:
            para.update(kwargs)
        res = {}
        response = api_sdk.BillQuery(para)
        try:
            res = json.loads(response)
            # _logger.info('生产领料单查询接口请求返回: {}'.format(res))
        except Exception as e:
            _logger.error('生产领料单查询接口请求返回错误: {}'.format(e))
        if len(res) > 0:
            for line in res:  # 遍历写入数据
                # 写入生产领料单数据
                material_record = material_obj.search([('MaterialId', '=', line['FMATERIALID'])])
                stock_record = stock_obj.search([('StockId', '=', line['FSTOCKID'])])
                workshop_record = stock_obj.search([('StockId', '=', line['FENTRYWORKSHOPID'])])
                unit_record = unit_obj.search([('UnitId', '=', line['FUNITID'])])
                stock_out_record = stock_out_obj.search([('TMBillNo', '=', line['FBILLNO']),
                                                         ('Order', '=', line['FMATERIALID'])])
                pv = {
                    'TMBillNo': line['FBILLNO'],
                    'Order': line['FMATERIALID'], # 由于云星空接口限制，取不到行号，用料号去唯一标识行号（同一张单据行料号不能出现重复情况）
                    'BillType': line['FFORMID'],
                    'MaterialId': material_record.id or False,
                    'XCode': material_record.XCode or False,
                    'XName': material_record.XName or False,
                    'Spec': material_record.Spec or False,
                    'Quantity': line['FACTUALQTY'] or False,
                    'UnitId': unit_record.id or False,
                    'UnitCode': unit_record.XCode or False,
                    'UnitName': unit_record.XName or False,
                    'BatchNo': line['FLOT.TEXT'] or False,
                    'CkStockId': stock_record.id or False,   # 调出仓库
                    'CkCode': stock_record.XCode or False,
                    'CkName': stock_record.XName or False,
                    'RkStockId': workshop_record.id or False,   # 调入仓库(生产车间)
                    'RkCode': workshop_record.XCode or False,
                    'RkName': workshop_record.id or False,
                    'DocumentStatus': line['FDOCUMENTSTATUS'],
                    'CancelStatus': line['FCANCELSTATUS'],
                    'SyncState': 0,
                }
                if stock_out_record and material_record and stock_out_record.SyncState == 1:
                    continue
                if stock_out_record and material_record and stock_out_record.SyncState == 0:
                    stock_out_record.write(pv)
                elif not stock_out_record and material_record:
                    stock_out_obj.create(pv)

    # =============== 简单生产领料单 ===============
    # =============== 简单生产领料单 ===============
    # =============== 简单生产领料单 ===============
    def Search_SP_PickMtrl_BillQuery(self):
        """
        本接口用于查旬业务状态为“审核中”的数据，去驱动WMS去搬运；
        AGV搬运完成后，调用接口将单据状态变更为“C已审核”确认库存
        21 中裕软管科技股份有限公司  库表ID：101124
        23 安徽优耐德管道技术有限公司  库表ID：101127
        "and FDOCUMENTSTATUS = 'B' "
        "and FCANCELSTATUS = 'A' "
        :return:
        """
        self.Data_SP_PickMtrl_BillQuery(Limit=100, FilterString="FBILLNO like '%%' "
                                                                "and FDocumentStatus = 'B' " "and FCancelStatus = 'A' "
                                                                "and FSTOCKORGID = '101127'" )

    def Data_SP_PickMtrl_BillQuery(self, **kwargs):
        """
        本接口用于实现简单生产领料单 (SP_PickMtrl) 的单据查询(json)功能
        :param kwargs:  替换para中参数，示例：FieldKeys=“Fname",Limit=1000
        :return:
        """
        stock_out_obj = self.env['wms.ship.order']  # 简单生产领料单
        material_obj = self.env['wms.material.info']
        stock_obj = self.env['wms.stock.info']  # 仓库
        unit_obj = self.env['wms.unit.info']
        para = {
            "FormId": "SP_PickMtrl",
            "FieldKeys": "FBILLNO, FFORMID, FMATERIALID, FUNITID, FSTOCKID, FWORKSHOPID, FACTUALQTY, FLOT, FLOT_TEXT, FDOCUMENTSTATUS, FCANCELSTATUS",
            "FilterString": "'FBILLNO'=""",
            "OrderString": "",
            "TopRowCount": 1000,
            "StartRow": 0,
            "Limit": 1000,
            "SubSystemId": ""
        }
        if kwargs:
            para.update(kwargs)
        res = {}
        response = api_sdk.BillQuery(para)
        try:
            res = json.loads(response)
            _logger.info('简单生产领料单查询接口请求返回: {}'.format(res))
        except Exception as e:
            _logger.error('简单生产领料单查询接口请求返回错误: {}'.format(e))
        if len(res) > 0:
            for line in res:  # 遍历写入数据
                # 写入简单生产领料单数据
                material_record = material_obj.search([('MaterialId', '=', line['FMATERIALID'])])
                stock_record = stock_obj.search([('StockId', '=', line['FSTOCKID'])])
                workshop_record = stock_obj.search([('StockId', '=', line['FWORKSHOPID'])])
                unit_record = unit_obj.search([('UnitId', '=', line['FUNITID'])])
                stock_out_record = stock_out_obj.search([('TMBillNo', '=', line['FBILLNO']),
                                                         ('Order', '=', line['FMATERIALID'])])
                pv = {
                    'TMBillNo': line['FBILLNO'],
                    'Order': line['FMATERIALID'], # 由于云星空接口限制，取不到行号，用料号去唯一标识行号（同一张单据行料号不能出现重复情况）
                    'BillType': line['FFORMID'],
                    'MaterialId': material_record.id or False,
                    'XCode': material_record.XCode or False,
                    'XName': material_record.XName or False,
                    'Spec': material_record.Spec or False,
                    'Quantity': line['FACTUALQTY'] or False,
                    'UnitId': unit_record.id or False,
                    'UnitCode': unit_record.XCode or False,
                    'UnitName': unit_record.XName or False,
                    'BatchNo': line['FLOT.TEXT'] or False,
                    'CkStockId': stock_record.id or False,   # 调出仓库
                    'CkCode': stock_record.XCode or False,
                    'CkName': stock_record.XName or False,
                    'RkStockId': False,   # 调入仓库(生产车间)
                    'RkCode': False,
                    'RkName': False,
                    'DocumentStatus': line['FDOCUMENTSTATUS'],
                    'CancelStatus': line['FCANCELSTATUS'],
                    'SyncState': 0,
                }
                if stock_out_record and material_record and stock_out_record.SyncState == 1:
                    continue
                if stock_out_record and material_record and stock_out_record.SyncState == 0:
                    stock_out_record.write(pv)
                elif not stock_out_record and material_record:
                    stock_out_obj.create(pv)

    # =============== 其他出库单 ===============
    # =============== 其他出库单 ===============
    # =============== 其他出库单 ===============
    def Search_Stk_MisDelivery_BillQuery(self):
        """
        本接口用于查旬业务状态为“审核中”的数据，去驱动WMS去搬运；
        AGV搬运完成后，调用接口将单据状态变更为“C已审核”确认库存
        21 中裕软管科技股份有限公司  库表ID：101124
        23 安徽优耐德管道技术有限公司  库表ID：101127
        "and FDOCUMENTSTATUS = 'B' "
        "and FCANCELSTATUS = 'A' "
        :return:
        """
        self.Data_Stk_MisDelivery_BillQuery(Limit=100, FilterString="FBILLNO like '%%' "
                                                                    "and FDocumentStatus = 'B' " "and FCancelStatus = 'A' "
                                                                    "and FSTOCKORGID = '101127'" )

    def Data_Stk_MisDelivery_BillQuery(self, **kwargs):
        """
        本接口用于实现简单生产领料单 (SP_PickMtrl) 的单据查询(json)功能
        :param kwargs:  替换para中参数，示例：FieldKeys=“Fname",Limit=1000
        :return:
        """
        stock_out_obj = self.env['wms.ship.order']  # 其他出库单
        material_obj = self.env['wms.material.info']
        stock_obj = self.env['wms.stock.info']  # 仓库
        unit_obj = self.env['wms.unit.info']
        para = {
            "FormId": "Stk_MisDelivery",
            "FieldKeys": "FBILLNO, FOBJECTTYPEID, FMATERIALID, FUNITID, FSTOCKID, FQTY, FLOT, FLOT_TEXT, FDOCUMENTSTATUS, FCANCELSTATUS",
            "FilterString": "'FBILLNO'=""",
            "OrderString": "",
            "TopRowCount": 1000,
            "StartRow": 0,
            "Limit": 1000,
            "SubSystemId": ""
        }
        if kwargs:
            para.update(kwargs)
        res = {}
        response = api_sdk.BillQuery(para)
        try:
            res = json.loads(response)
            _logger.info('其他出库单查询接口请求返回: {}'.format(res))
        except Exception as e:
            _logger.error('其他出库单查询接口请求返回错误: {}'.format(e))
        if len(res) > 0:
            for line in res:  # 遍历写入数据
                # 写入其他出库单数据
                material_record = material_obj.search([('MaterialId', '=', line['FMATERIALID'])])
                stock_record = stock_obj.search([('StockId', '=', line['FSTOCKID'])])
                unit_record = unit_obj.search([('StockId', '=', line['FUNITID'])])
                stock_out_record = stock_out_obj.search([('TMBillNo', '=', line['FBILLNO']),
                                                         ('Order', '=', line['FMATERIALID'])])
                pv = {
                    'TMBillNo': line['FBILLNO'],
                    'Order': line['FMATERIALID'], # 由于云星空接口限制，取不到行号，用料号去唯一标识行号（同一张单据行料号不能出现重复情况）
                    'BillType': line['FOBJECTTYPEID'],
                    'MaterialId': material_record.id or False,
                    'XCode': material_record.XCode or False,
                    'XName': material_record.XName or False,
                    'Spec': material_record.Spec or False,
                    'Quantity': line['FQTY'] or False,
                    'UnitId': unit_record.id or False,
                    'UnitCode': unit_record.XCode or False,
                    'UnitName': unit_record.XName or False,
                    'BatchNo': line['FLOT.TEXT'] or False,
                    'CkStockId': stock_record.id or False,   # 调出仓库
                    'CkCode': stock_record.XCode or False,
                    'CkName': stock_record.XName or False,
                    'RkStockId': False,   # 调入仓库(生产车间)
                    'RkCode': False,
                    'RkName': False,
                    'DocumentStatus': line['FDOCUMENTSTATUS'],
                    'CancelStatus': line['FCANCELSTATUS'],
                    'SyncState': 0,
                }
                if stock_out_record and material_record and stock_out_record.SyncState == 1:
                    continue
                if stock_out_record and material_record and stock_out_record.SyncState == 0:
                    stock_out_record.write(pv)
                elif not stock_out_record and material_record:
                    stock_out_obj.create(pv)