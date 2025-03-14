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

    # =============== 从ERP查询订单数据 到中间平台 加受控水印回传云星空 ===============
    # =============== 从ERP查询订单数据 到中间平台 加受控水印回传云星空 ===============
    # =============== 从ERP查询订单数据 到中间平台 加受控水印回传云星空 ===============
    def Action_Sale_BillQuery(self):
        """
        本接口用于实现的单据查询(json)功能
        :param kwargs:  替换para中参数，示例：FieldKeys=“Fname",Limit=1000
        :return:

        "and FDocumentStatus = 'C' "
        """
        self.Search_SaleOrder_BillQuery(Limit=20,
                                        FilterString="FBILLNO like '%%' "   
                                                     "and FDocumentStatus = 'C' "
                                                     "and FCancelStatus = 'A' ")  # 查销售订单

    # =============== 销售订单 走中间平台 加受控水印回传云星空 ===============
    # =============== 销售订单 走中间平台 加受控水印回传云星空 ===============
    # =============== 销售订单 走中间平台 加受控水印回传云星空 ===============
    def Search_SaleOrder_BillQuery(self, **kwargs):
        """
        本接口用于实现销售订单(SAL_ORDER) 的单据查询(json)功能
        :param kwargs:  替换para中参数，示例：FieldKeys=“Fname",Limit=1000
        :return:
        """
        approval_obj = self.env['qstamper.approval']
        para = {
            "FormId": "SAL_SaleOrder",
            "FieldKeys": "FID, FBILLNO, FOBJECTTYPEID, FSALERID, FDATE, FDOCUMENTSTATUS, FCANCELSTATUS, F_ZOYO_ATTACHMENT1",
            "FilterString": "'FNumber'=""",
            "OrderString": "FDATE DESC",
            "TopRowCount": 20,
            "StartRow": 0,
            "Limit": 20,
            "SubSystemId": ""
        }
        if kwargs:
            para.update(kwargs)
        response = api_sdk.BillQuery(para)
        res = {}
        try:
            res = json.loads(response)
        except Exception as e:
            _logger.error('受控水印：销售订单请求云星空单据查询接口错误: {}'.format(e))
        tot_len = int(len(res) / 100 + 1)
        start = 0
        end = 100
        if len(res) > 0:
            for ci in range(0, tot_len):
                records2 = res[start:end]
                if not records2:
                    continue
                for line in records2:  # 遍历写入数据
                    _logger.info('当前请求加受控水印单据号: {}'.format(line['FBILLNO']))
                    approval_record = approval_obj.search([('name', '=', line['FBILLNO']), ('ControlState', '=', True)])   # 查有没有相同数据。有，修改；没有，创建。
                    if approval_record:
                        _logger.info('单据号 {} 已存在，跳过加水印过程!'.format(line['FBILLNO']))
                        continue
                    # 判断有附件字段，则拿附件去加受控水印
                    attachment = line.get('F.ZOYO.ATTACHMENT1')
                    # 判断字段是否为空，这里考虑了多种空的情况，如空字符串、None、空列表、空字典等
                    if not attachment:
                        continue
                    # 处理加控附件返回结果
                    result = self.Search_attachmentDownLoad(line['F.ZOYO.ATTACHMENT1'], line['FBILLNO'])
                    if result is None:
                        continue  # 如果返回 None，跳过当前循环后续操作，继续下一次循环
                    # 处理返回结果
                    attach_size, source_attach_name, source_binary_data, dest_attach_name, dest_attach_data = result
                    pv = {
                        'name': line['FBILLNO'],
                        'BillType': line['FOBJECTTYPEID'],
                        'applicant': line['FSALERID'],
                        'category': False,
                        'date': line['FDATE'],
                        'SyncState': False,
                        'ControlState': True,
                        'DocumentStatus': line['FDOCUMENTSTATUS'],
                        'CancelStatus': line['FCANCELSTATUS'],
                        'attachment_id': line['FID'],
                        'FileSize': attach_size or False,
                        'source_binary_data': source_binary_data or False,  # 生产单附件 Binary类型
                        'source_binary_data_name': source_attach_name or False,
                        'dest_attach_data': dest_attach_data or False,  # 生产单附件 Binary类型
                        'dest_binary_data_name': dest_attach_name or False,
                    }
                    if not approval_record:
                        approval_obj.create(pv)
                    try:
                        # 从ERP查询订单数据 到中间平台 回馈附件给云星空
                        self.Search_attachmentUpload(line['FID'], line['FBILLNO'])
                    except Exception as e:
                        _logger.error(f"回馈附件给云星空错误: {e}")
                        continue
                    _logger.info('单据号 {} 增加受控水印成功!'.format(line['FBILLNO']))
                start = end
                end = end + 100
