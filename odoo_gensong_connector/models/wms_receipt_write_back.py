# -*- coding: utf-8 -*-
"""
@Time    : 2024/12/05 8:20
@Author  : Jason Zou
@Email   : zou.jason@qq.com
@mobile  : 18951631470
"""
import json, time, logging, datetime
import pymssql
from odoo import api, fields, models
from .k3cloud_conn import *
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
    def Action_StockIn_Write_Back(self):
        try:
            self.Search_StockIn_Write_Back()    # 审核采购入库单
            # self.Search_Prd_InStock_Write_Back()  # 审核生产入库单
            self.Search_Prd_Mo_Write_Back()  # 调用下推生产订单下推生产入库单接口 并审核生产入库单
        except Exception as e:
            _logger.error('接口返回结果：{}'.format(e))

    # =============== 审核采购入库单 ===============
    # =============== 审核采购入库单 ===============
    # =============== 审核采购入库单 ===============
    def Search_StockIn_Write_Back(self):
        """
        本接口用于实现采购入库单 (STK_INSTOCK)  的 C审核 功能
        21 中裕软管科技股份有限公司  库表ID：101124
        23 安徽优耐德管道技术有限公司  库表ID：101127

        "and FDocumentStatus = 'B' " "and FCancelStatus = 'A' "
        search_data = stock_in_obj.search([
            ('create_date', '>=', today.strftime('%Y-%m-%d 00:00:00')),
            ('create_date', '<=', today.strftime('%Y-%m-%d 23:59:59')),
            ('SyncState', '=', 1),
            ('DocumentStatus', '=', 'B')
        ])
        :return:
        """
        stock_in_obj = self.env['wms.receipt.order']  # 采购入库单
        # 查数据
        # today = datetime.date.today()
        _logger.info('采购入库接口回写--当前时间：{}'.format(datetime.datetime.utcnow() + datetime.timedelta(hours=8)))
        search_data = stock_in_obj.search([('SyncState', '=', 1), ('DocumentStatus', '=', 'B')])
        check_values = []
        result = []
        _logger.info('采购入库接口回写--传递数据：'.format(search_data))
        if len(search_data) == 0:
            return
        for line in search_data:
            check_values.append(line.TMBillNo)
        for value in sorted(list(set(check_values))):
            li = stock_in_obj.search([('TMBillNo', '=', value)])
            check_values1 = []
            for l in li:
                check_values1.append(l.SyncState)
            if len(list(set(check_values1))) == 1:
                result.append(l.TMBillNo)
            # 判断AGV是否执行完，搬运完成整单回写提交ERP采购入库单审核
        _logger.info('采购入库接口回写--更新记录：'.format(sorted(list(set(result)))))
        self.Data_StockIn_Write_Back(Numbers=result)    # 批量提交云星空单据审批，变更状态为“C已审批”
        for tmp in result:
            c = stock_in_obj.search([('TMBillNo', '=', tmp)])
            c.write({'DocumentStatus': 'C'})    # 批量变更本地单据状态，变更状态为“C已审批”

    def Data_StockIn_Write_Back(self, **kwargs):
        """
        本接口用于实现采购入库单 (STK_INSTOCK)  的审核功能
        :param kwargs:  替换para中参数，示例：   Numbers = []
        :return:
        """
        para = {"CreateOrgId": 0,
                "Numbers": [],
                "Ids": "",
                "SelectedPostId": 0,
                "NetworkCtrl": "",
                "IgnoreInterationFlag": "",
                "IsVerifyProcInst": "",
                }
        if kwargs:
            para.update(kwargs)
        response = api_sdk.Audit("STK_INSTOCK", para)
        res = json.loads(response)
        return res

    # =============== 回写生产入库单 ===============
    # =============== 回写生产入库单 ===============
    # =============== 回写生产入库单 ===============
    def Search_Prd_InStock_Write_Back(self):
        """
        本接口用于查旬业务状态为“审核中”的数据，去驱动WMS去搬运；
        AGV搬运完成后，调用接口将单据状态变更为“C已审核”确认库存
        21 中裕软管科技股份有限公司  库表ID：101124
        23 安徽优耐德管道技术有限公司  库表ID：101127

        "and FDocumentStatus = 'B' " "and FCancelStatus = 'A' "

        search_data = stock_in_obj.search([
            # ('create_date', '>=', today.strftime('%Y-%m-%d 00:00:00')),
            # ('create_date', '<=', today.strftime('%Y-%m-%d 23:59:59')),
            ('SyncState', '=', 1),
            ('DocumentStatus', '=', 'B')
        ])
        :return:
        """
        stock_in_obj = self.env['wms.receipt.order']  # 采购入库单
        # 查数据
        # today = datetime.date.today()
        _logger.info('生产入库接口回写--当前时间：{}'.format(datetime.datetime.utcnow() + datetime.timedelta(hours=8)))
        search_data = stock_in_obj.search([('SyncState', '=', 1), ('DocumentStatus', '=', 'B')])
        check_values = []
        result = []
        _logger.info('生产入库接口回写--传递数据：'.format(search_data))
        if len(search_data) == 0:
            return
        for line in search_data:
            check_values.append(line.TMBillNo)
        for value in sorted(list(set(check_values))):
            li = stock_in_obj.search([('TMBillNo', '=', value)])
            check_values1 = []
            for l in li:
                check_values1.append(l.SyncState)
            if len(list(set(check_values1))) == 1:
                result.append(l.TMBillNo)
            # 判断AGV是否执行完，搬运完成整单回写提交ERP采购入库单审核
        _logger.info('生产入库接口回写--更新记录：'.format(sorted(list(set(result)))))
        self.Data_Prd_InStock_Write_Back(Numbers=result)  # 批量提交云星空单据审批，变更状态为“C已审批”
        for tmp in result:
            c = stock_in_obj.search([('TMBillNo', '=', tmp)])
            c.write({'DocumentStatus': 'C'})  # 批量变更本地单据状态，变更状态为“C已审批”

    def Data_Prd_InStock_Write_Back(self, **kwargs):
        """
        本接口用于实现生产入库单 (PRD_INSTOCK) 的单据查询(json)功能
        :param kwargs:  替换para中参数，示例：FieldKeys=“Fname",Limit=1000
        :return:
        """
        para = {"CreateOrgId": 0,
                "Numbers": [],
                "Ids": "",
                "SelectedPostId": 0,
                "NetworkCtrl": "",
                "IgnoreInterationFlag": "",
                "IsVerifyProcInst": "",
                }
        if kwargs:
            para.update(kwargs)
        response = api_sdk.Audit("PRD_INSTOCK", para)
        res = json.loads(response)
        return res


    # =============== 调用下推生产订单下推生产入库单接口 并审核生产入库单 ===============
    # =============== 调用下推生产订单下推生产入库单接口 并审核生产入库单 ===============
    # =============== 调用下推生产订单下推生产入库单接口 并审核生产入库单 ===============
    def Search_Prd_Mo_Write_Back(self):
        """
        本接口用于查旬业务状态为“审核中”的数据，去驱动WMS去搬运；
        AGV搬运完成后，调用接口将单据状态变更为“C已审核”确认库存
        21 中裕软管科技股份有限公司  库表ID：101124
        23 安徽优耐德管道技术有限公司  库表ID：101127

        "and FDocumentStatus = 'B' " "and FCancelStatus = 'A' "

        search_data = stock_in_obj.search([
            # ('create_date', '>=', today.strftime('%Y-%m-%d 00:00:00')),
            # ('create_date', '<=', today.strftime('%Y-%m-%d 23:59:59')),
            ('SyncState', '=', 1),
            ('DocumentStatus', '=', 'B')
        ])
        :return:
        """
        stock_in_obj = self.env['wms.receipt.order']  # 生产订单下推生产入库单
        # 查数据
        # today = datetime.date.today()
        _logger.info('生产订单接口回写--当前时间：{}'.format(datetime.datetime.utcnow() + datetime.timedelta(hours=8)))
        search_data = stock_in_obj.search([('SyncState', '=', 1), ('DocumentStatus', '=', 'C')])
        check_values = []
        result = []
        _logger.info('生产订单接口回写--传递数据：{}'.format(search_data))
        if len(search_data) == 0:
            _logger.info('生产订单接口回写--没有查询到待回写的数据')
            return
        for line in search_data:
            check_values.append(line.TMBillNo)
        for value in sorted(list(set(check_values))):
            li = stock_in_obj.search([('TMBillNo', '=', value)])
            check_values1 = []
            for l in li:
                check_values1.append(l.SyncState)
            if len(list(set(check_values1))) == 1:
                result.append(l.TMBillNo)
            # 判断AGV是否执行完，搬运完成整单回写提交ERP采购入库单审核
        _logger.info('生产订单接口回写--更新记录：{}'.format(sorted(list(set(result)))))
        self.Data_Prd_Mo_Write_Back(Numbers=result)  # 批量提交云星空单据审批，变更状态为“C已审批”
        # for tmp in result:
        #     c = stock_in_obj.search([('TMBillNo', '=', tmp)])
        #     c.write({'DocumentStatus': 'D'})  # 批量变更本地单据状态，变更状态为“C已审批”

    def Data_Prd_Mo_Write_Back(self, **kwargs):
        """
        本接口用于实现生产订单下推生产入库单 (PRD_MO2INSTOCK) 的(json)功能
        动作一：调用下推接口生成保存状态的生产入库单
        动作二：调用修改生产入库单接口，修改里面的内容；
        动作三：调用审核接口将数据提交审核完成
        :param kwargs:  替换para中参数，示例：FieldKeys=“Fname",Limit=1000
        :return:
        """
        for kwarg in kwargs['Numbers']:
            _logger.info('当前下推生产订单号为：{}'.format(kwarg))
            receipt_obj = self.env['wms.receipt.order']  # 生产订单下推生产入库单
            receipt_records = receipt_obj.search([('TMBillNo', '=', kwarg)])
            FEntryIds = []
            for li in receipt_records:
                FEntryIds.append(li.FEntryID)
            para = {
                "Ids": "",
                "Numbers": kwarg,
                "EntryIds": FEntryIds,
                "RuleId": "PRD_MO2INSTOCK",
                "TargetBillTypeId": "",
                "TargetOrgId": 101127,
                "TargetFormId": "PRD_INSTOCK",
                "IsEnableDefaultRule": "false",
                "IsDraftWhenSaveFail": "true",
                "CustomParams": {
                    # 'FSTOCKID': '114333',
                    # 'FLOT_TEXT': '222220',
                    # 'FAUXPROPID': '100514',
                    # 'FSTOCKSTATUSID': '10000'
                }    # 自定义参数，字典类型，（非必录）注（传到转换插件的操作选项中，平台不会解析里面的值）
            }
            res = {}
            try:
                if kwargs:
                    para.update(kwargs)
                response = api_sdk.Push("PRD_MO", para)  # 动作一：调用下推接口生成保存状态的生产入库单
                res = json.loads(response)
                _logger.info('生产订单下推生产入库单记录：{}'.format(res))
                # self.Data_Prd_Instock_Save(Numbers=kwarg)  # 动作二：调用修改生产入库单接口，修改里面的内容；
                # self.Data_Prd_Instock_Audit(Numbers=kwarg)  # 动作三：调用审核接口将数据提交审核完成
                return res
            except Exception as e:
                _logger.error(res)
                continue

    def Data_Prd_Instock_Save(self, **kwargs):
        """
        本接口用于实现生产订单下推生产入库单 (PRD_MO2INSTOCK) 的(json)功能
        动作二：调用修改生产入库单接口，修改里面的内容；
        :param kwargs:  替换para中参数，示例：FieldKeys=“Fname",Limit=1000
        :return:
        """
        _logger.info("host={}  user={}  password={} database={} ".format(host, user, password, database))
        ms_conn = pymssql.connect(
            host="%s" % host,
            user="%s" % user,
            password="%s" % password,
            database="%s" % database,
            charset="utf8")
        ms_cursor = ms_conn.cursor()  # 输出从SHR拿回来的记录集
        # 检查是否有匹配的记录
        check_sql = "SELECT COUNT(*) FROM T_PRD_INSTOCKENTRY WHERE FMOBILLNO = '{}'".format(kwargs['Numbers'])
        try:
            ms_cursor.execute(check_sql)
            count = ms_cursor.fetchone()[0]
            if count == 0:
                print("没有匹配的记录，无法更新。")
            else:
                update_sql = """
                    UPDATE
                        T_PRD_INSTOCKENTRY
                    SET
                        FSTOCKID = '114333',
                        FLOT_TEXT = '222220',
                        FAUXPROPID = '100514',
                        FSTOCKSTATUSID = '10000'
                    WHERE FMOBILLNO = '{}'
                """.format(kwargs['Numbers'])
                print(update_sql)
                ms_cursor.execute(update_sql)
                ms_conn.commit()  # 提交事务
        except pymssql.Error as e:
            _logger.error('执行 SQL 语句时出错: %s', e)
            ms_conn.rollback()  # 回滚事务
        finally:
            if ms_conn:
                ms_conn.close()

    def Data_Prd_Instock_Submit(self, **kwargs):
        para = {
            "CreateOrgId": 0,
            "Numbers": [],
            "Ids": "",
            "SelectedPostId": 0,
            "NetworkCtrl": "",
            "IgnoreInterationFlag": ""
        }
        if kwargs:
            para.update(kwargs)
        response = api_sdk.Audit("PRD_INSTOCK", para)
        res = json.loads(response)
        return res



