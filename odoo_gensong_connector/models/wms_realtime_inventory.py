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

# 首先构造一个SDK实例
api_sdk = K3CloudApiSdk()
# config_node:配置文件中的节点名称
api_sdk.Init(config_path='rhino-data-nexus/sdk/conf.ini', config_node='config')
# 此处仅构造保存接口的部分字段数据示例，使用时请参考WebAPI具体接口的实际参数列表
current_time = time.strftime('%Y%m%d%H%M%S', time.localtime())


class WmsRealtimeInventory(models.Model):
    _inherit = 'wms.realtime.inventory'

    # =============== 即时库存表同步 ===============
    # =============== 即时库存表同步 ===============
    # =============== 即时库存表同步 ===============
    def action_realtime_inventory(self):
        try:
            self.Search_Stk_Inventory_BillQuery()    # 即时库存表
        except Exception as e:
            _logger.error('接口返回结果：{}'.format(e))

    # =============== 即时库存表 ===============
    # =============== 即时库存表 ===============
    # =============== 即时库存表 ===============
    def Search_Stk_Inventory_BillQuery(self):
        """
        本接口用于查旬业务状态为“审核中”的数据，去驱动WMS去搬运；
        AGV搬运完成后，调用接口将单据状态变更为“C已审核”确认库存
        21 中裕软管科技股份有限公司  库表ID：101124
        23 安徽优耐德管道技术有限公司  库表ID：101127
        :return:
        """
        self.Data_Stk_Inventory_BillQuery(Limit=10000, FilterString="FStockOrgId = '101127'")

    def Data_Stk_Inventory_BillQuery(self, **kwargs):
        """
        本接口用于实现即时库存表 (STK_STKTRANSFERIN) 的单据查询(json)功能
        :param kwargs:  替换para中参数，示例：FieldKeys=“Fname",Limit=1000
        :return:
        """
        realtime_inventory_obj = self.env['wms.realtime.inventory']  # 销售出库单
        material_obj = self.env['wms.material.info']
        stock_obj = self.env['wms.stock.info']  # 仓库
        unit_obj = self.env['wms.unit.info']
        para = {
            "FormId": "STK_INVENTORY",
            "FieldKeys": "FID, FOBJECTTYPEID, FStockOrgId, FStockId, FMaterialId, FLot, FBaseUnitid, FBaseQty, FBaseLockQty",
            "FilterString": "'FStockOrgId'=""",
            "OrderString": "",
            "TopRowCount": 10000,
            "StartRow": 0,
            "Limit": 10000,
            "SubSystemId": ""
        }
        if kwargs:
            para.update(kwargs)
        response = api_sdk.BillQuery(para)
        res = json.loads(response)
        tot_len = int(len(res) / 1000 + 1)
        start = 0
        end = 1000
        if len(res) > 0:
            for ci in range(0, tot_len):
                records2 = res[start:end]
                if not records2:
                    continue
                for line in records2:  # 遍历写入数据
                    # 写入即时库存表数据
                    material_record = material_obj.search([('MaterialId', '=', line['FMaterialId'])])
                    warehouse_record = stock_obj.search([('StockId', '=', line['FStockId'])])
                    unit_record = unit_obj.search([('UnitId', '=', line['FBaseUnitid'])])
                    realtime_inventory_record = realtime_inventory_obj.search([('FID', '=', line['FID'])])
                    pv = {
                        'FID': line['FID'],
                        'BillType': line['FOBJECTTYPEID'],
                        'StockOrgId': line['FStockOrgId'],
                        'StockId': warehouse_record.id,
                        'StockCode': warehouse_record.XCode or False,
                        'StockName': warehouse_record.XName or False,
                        'MaterialId': material_record.id or False,
                        'MaterialCode': material_record.XCode or False,
                        'MaterialName': material_record.XName or False,
                        'Spec': material_record.Spec or False,
                        'BatchNo': line['FLot'],
                        'UnitId': unit_record.id or False,
                        'UnitCode': unit_record.XCode or False,
                        'UnitName': unit_record.XName or False,
                        'BaseQty': line['FBaseQty'],
                        'BaseLockQty': line['FBaseLockQty'],
                        'SyncState': 0,
                    }
                    if realtime_inventory_record and material_record:
                        realtime_inventory_record.write(pv)
                    elif not realtime_inventory_record and material_record:
                        realtime_inventory_obj.create(pv)
                start = end
                end = end + 1000