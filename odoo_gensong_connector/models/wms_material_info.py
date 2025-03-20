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


class WmsMaterialInfo(models.Model):
    _inherit = 'wms.material.info'

    # =============== 车间（部门主档） ===============
    # =============== 车间（部门主档） ===============
    # =============== 车间（部门主档） ===============
    def action_Dept_BillQuery(self):
        self.Dept_BillQuery(Limit=2000, FilterString="FNumber like '23%'")

    def Dept_BillQuery(self, **kwargs):
        """
        本接口用于实现生产车间（工作中心）信息 (ENG_WORKCENTER) 的单据查询(json)功能
        :param kwargs:  替换para中参数，示例：FieldKeys=“Fname",Limit=1000
        :return:
        """
        dept_obj = self.env['wms.stock.info']
        para = {
            "FormId": "BD_DEPARTMENT",
            "FieldKeys": "FDEPTID, FNUMBER, FNAME, FDOCUMENTSTATUS, FFORBIDSTATUS",
            "FilterString": "'FNumber'=""",
            "OrderString": "",
            "TopRowCount": 2000,
            "StartRow": 0,
            "Limit": 2000,
            "SubSystemId": ""
        }
        if kwargs:
            para.update(kwargs)
        response = api_sdk.BillQuery(para)
        # print("生产车间查询接口：" + response)
        res = json.loads(response)
        if len(res) > 0:
            for line in res:  # 遍历写入数据
                # 写入工作中心
                dept_record = dept_obj.search([('StockId', '=', line['FDEPTID']), ('Spec', '=', '车间')])
                pv = {
                    'StockId': line['FDEPTID'],
                    'XCode': line['FNUMBER'],
                    'XName': line['FNAME'],
                    'Spec': '车间',
                    'DocumentStatus': line['FDOCUMENTSTATUS'],
                    'ForbidStatus': line['FFORBIDSTATUS'],
                }
                if dept_record:
                    dept_record.write(pv)
                else:
                    dept_obj.create(pv)

    # =============== 仓库信息 ===============
    # =============== 仓库信息 ===============
    # =============== 仓库信息 ===============
    def action_Stock_BillQuery(self):
        self.Stock_BillQuery(Limit=2000, FilterString="FNumber like '%%'")

    def Stock_BillQuery(self, **kwargs):
        """
        本接口用于实现仓库信息 (BD_Stock) 的单据查询(json)功能
        :param kwargs:  替换para中参数，示例：FieldKeys=“Fname",Limit=1000
        :return:
        """
        para = {
            "FormId": "BD_Stock",
            "FieldKeys": "FStockId, FNUMBER, FNAME, FDOCUMENTSTATUS, FFORBIDSTATUS",
            "FilterString": "'FNumber'=""",
            "OrderString": "",
            "TopRowCount": 2000,
            "StartRow": 0,
            "Limit": 2000,
            "SubSystemId": ""
        }
        if kwargs:
            para.update(kwargs)
        response = api_sdk.BillQuery(para)
        # print("仓库查询接口：" + response)
        res = json.loads(response)
        stock_obj = self.env['wms.stock.info']
        if len(res) > 0:
            for line in res:  # 遍历写入数据
                # 写入仓库
                stock_record = stock_obj.search([('StockId', '=', line['FStockId']), ('Spec', '=', '仓库')])
                pv = {
                    'StockId': line['FStockId'],
                    'XCode': line['FNUMBER'],
                    'XName': line['FNAME'],
                    'Spec': '仓库',
                    'DocumentStatus': line['FDOCUMENTSTATUS'],
                    'ForbidStatus': line['FFORBIDSTATUS'],
                }
                if stock_record:
                    stock_record.write(pv)
                else:
                    stock_obj.create(pv)

    # =============== 物料单位 ===============
    # =============== 物料单位 ===============
    # =============== 物料单位 ===============
    def action_Unit_BillQuery(self):
        self.Unit_BillQuery(Limit=2000, FilterString="FNumber like '%%'")

    def Unit_BillQuery(self, **kwargs):
        """
        本接口用于实现计量单位 (BD_Unit) 的单据查询(json)功能
        :param kwargs:  替换para中参数，示例：FieldKeys=“Fname",Limit=1000
        :return:
        """
        para = {
            "FormId": "BD_Unit",
            "FieldKeys": "FUNITID, FNUMBER, FNAME, FDOCUMENTSTATUS, FFORBIDSTATUS",
            "FilterString": "'FNumber'=""",
            "OrderString": "",
            "TopRowCount": 2000,
            "StartRow": 0,
            "Limit": 2000,
            "SubSystemId": ""
        }
        if kwargs:
            para.update(kwargs)
        response = api_sdk.BillQuery(para)
        # print("物料单位查询接口：" + response)
        res = json.loads(response)
        unit_obj = self.env['wms.unit.info']
        if len(res) > 0:
            for line in res:  # 遍历写入数据
                # 写入物料单位
                unit_record = unit_obj.search([('UnitId', '=', line['FUNITID'])])
                pv = {
                    'UnitId': line['FUNITID'],
                    'XCode': line['FNUMBER'],
                    'XName': line['FNAME'],
                    'DocumentStatus': line['FDOCUMENTSTATUS'],
                    'ForbidStatus': line['FFORBIDSTATUS'],
                }
                if unit_record:
                    unit_record.write(pv)
                else:
                    unit_obj.create(pv)

    # =============== 物料分类 ===============
    # =============== 物料分类 ===============
    # =============== 物料分类 ===============
    def action_Category_BillQuery(self):
        self.Category_BillQuery(Limit=2000, FilterString="FNumber like '%%'")

    def Category_BillQuery(self, **kwargs):
        """
        本接口用于实现物料分类 (BD_MaterialCategory) 的单据查询(json)功能
        :param kwargs:  替换para中参数，示例：FieldKeys=“Fname",Limit=1000
        :return:
        """
        para = {
            "FormId": "BD_MaterialCategory",
            "FieldKeys": "FCATEGORYID, FNUMBER, FNAME, FDOCUMENTSTATUS, FFORBIDSTATUS",
            "FilterString": "'FNumber'=""",
            "OrderString": "",
            "TopRowCount": 2000,
            "StartRow": 0,
            "Limit": 2000,
            "SubSystemId": ""
        }
        if kwargs:
            para.update(kwargs)
        response = api_sdk.BillQuery(para)
        # print("物料分类查询接口：" + response)
        res = json.loads(response)
        category_obj = self.env['wms.category.info']
        if len(res) > 0:
            for line in res:  # 遍历写入数据
                # 写入物料分类
                category_record = category_obj.search([('CategoryId', '=', line['FCATEGORYID'])])
                pv = {
                    'CategoryId': line['FCATEGORYID'],
                    'XCode': line['FNUMBER'],
                    'XName': line['FNAME'],
                    'DocumentStatus': line['FDOCUMENTSTATUS'],
                    'ForbidStatus': line['FFORBIDSTATUS'],
                }
                if category_record:
                    category_record.write(pv)
                else:
                    category_obj.create(pv)

    # =============== 物料 ===============
    # =============== 物料 ===============
    # =============== 物料 ===============
    def action_material_BillQuery(self):
        try:
            self.action_Stock_BillQuery()    # 查仓库
            self.action_Unit_BillQuery()    # 查物料单位
            self.action_Category_BillQuery()    # 查物料类别
            self.action_Dept_BillQuery()    # 查生产车间(工作中心)
            fn = ['10%', '20%', '21%', '22%', '24%', '30%', '31%', '37%']
            for ci in fn:
                self.Material_BillQuery(Limit=10000, FilterString="FNumber like '{}' and  FUSEORGID in ('101127', '1')".format(ci))  # 查物料信息
        except Exception as e:
            _logger.error('接口返回结果：{}'.format(e))

    def Material_BillQuery(self, **kwargs):
        """
        本接口用于实现物料 (BD_MATERIAL) 的单据查询(json)功能
        :param kwargs:  替换para中参数，示例：FieldKeys=“Fname",Limit=1000
        :return:
        """
        material_obj = self.env['wms.material.info']
        unit_obj = self.env['wms.unit.info']
        category_obj = self.env['wms.category.info']
        para = {
            "FormId": "BD_Material",
            "FieldKeys": "FUSEORGID, FMATERIALID, FNUMBER, FNAME, FSPECIFICATION, FBASEUNITID, FCATEGORYID, FMAXSTOCK, FMINSTOCK, FDOCUMENTSTATUS, FFORBIDSTATUS",
            "FilterString": "'FNumber'=""",
            "OrderString": "",
            "TopRowCount": 10000,
            "StartRow": 0,
            "Limit": 10000,
            "SubSystemId": ""
        }
        if kwargs:
            para.update(kwargs)
        response = api_sdk.BillQuery(para)
        # print("物料单据查询接口：" + response)
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
                    # 写入物料数据
                    material_record = material_obj.search([('MaterialId', '=', line['FMATERIALID'])])
                    unit_record = unit_obj.search([('UnitId', '=', line['FBASEUNITID'])])
                    category_record = category_obj.search([('CategoryId', '=', line['FCATEGORYID'])])
                    pv = {
                        'MaterialId': line['FMATERIALID'],
                        'XCode': line['FNUMBER'],
                        'XName': line['FNAME'],
                        'Spec': line['FSPECIFICATION'],
                        'Class': category_record.id or False,
                        'SmallestUnit': unit_record.id or False,
                        'Upper': line['FMAXSTOCK'],
                        'Lower': line['FMINSTOCK'],
                        'Days': False,
                        'DocumentStatus': line['FDOCUMENTSTATUS'],
                        'ForbidStatus': line['FFORBIDSTATUS'],
                        'SyncState': 0,
                    }
                    if material_record:
                        material_record.write(pv)
                    else:
                        material_obj.create(pv)
                start = end
                end = end + 1000