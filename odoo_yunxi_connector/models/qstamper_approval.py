# -*- coding: utf-8 -*-
"""
@Time    : 2025/1/6 8:20
@Author  : Jason Zou
@Email   : zou.jason@qq.com
@mobile  : 18951631470
"""
from odoo import api, fields, models
import json, requests
import logging
import time
import uuid
_logger = logging.getLogger(__name__)

current_time = time.strftime('%Y%m%d%H%M%S', time.localtime())


class QstamperEquipment(models.Model):
    _inherit = 'qstamper.equipment'

    def gen_data_from_yunxi(self):
        token_obj = self.env['yunxi.token']
        equipment_obj = self.env['qstamper.equipment']
        token_record = token_obj.search([('name', '=', '获取云玺平台接口调用token')])

        appKey = token_record.appKey  # 应用标识
        # appSecret = token_record.appSecret  # 应用秘钥
        tenant = token_record.tenant  # 租户标识
        # unique_id = uuid.uuid4()    # 生成 UUID
        # unique_id_str = str(unique_id)
        timestamp_milliseconds = int(time.time() * 1000)          # 获取当前时间的毫秒级时间戳

        url = ''
        try:
            if token_record.url and token_record.port:
                url = token_record.url + ':' + token_record.port + '/stamper/apis/business/docking/execute'  # 授权处理
        except Exception as e:
            _logger.error(f'{e}')
            return
        headers = {"Content-Type": "application/json; charset=UTF-8", 'Connection': 'close'}

        data = {  # 获取印章设备信息
            "appKey": appKey,  # 应用标识，接入的应用系统身份标识,由印管平台提供
            "apiKey": "YXYG04_01",  # 接口标识，详细接口标识请参见接口标识
            "timestamp": timestamp_milliseconds,  # 时间戳，本次请求时间戳,单位:毫秒值
            "bizId": '2d23a78864ca4344976fa848594c27bb',  # 业务标识，本次请求业务标识,推荐使用UUID.randomUUID().toString()
            "tenant": tenant,  # 租户标识，由印管平台提供
            "params": "{'pageNum':1,'pageSize':10}"  # 应用标识
        }
        response = requests.post(url, data=json.dumps(data), headers=headers)  # 定义以JSON格式发送数据
        res = json.loads(response.text)
        # print(res)

        try:
            for line in res['data']['list']:
                equipment_record = equipment_obj.search([('uuid', '=', line['uuid'])])  # 查有没有相同数据。有，修改；没有，创建。
                pv = {
                    'name': line['name'],
                    'uuid': line['uuid'],
                    'tenant': line['tenant'],
                    'deptName': line['deptName'],
                    'location': line['location'],
                    'type': line['type'],
                    'online': line['online'],
                }
                if equipment_record:
                    equipment_record.write(pv)
                else:
                    equipment_obj.create(pv)
        except Exception as e:
            _logger.error(f'{e}')
            return


class QstamperFileType(models.Model):
    _inherit = 'qstamper.file.type'

    def gen_data_from_yunxi(self):
        token_obj = self.env['yunxi.token']
        type_obj = self.env['qstamper.file.type']
        token_record = token_obj.search([('name', '=', '获取云玺平台接口调用token')])

        appKey = token_record.appKey  # 应用标识
        # appSecret = token_record.appSecret  # 应用秘钥
        tenant = token_record.tenant  # 租户标识
        # unique_id = uuid.uuid4()    # 生成 UUID
        # unique_id_str = str(unique_id)
        timestamp_milliseconds = int(time.time() * 1000)          # 获取当前时间的毫秒级时间戳

        url = ''
        try:
            if token_record.url and token_record.port:
                url = token_record.url + ':' + token_record.port + '/stamper/apis/business/docking/execute'  # 授权处理
        except Exception as e:
            _logger.error(f'{e}')
            return
        headers = {"Content-Type": "application/json; charset=UTF-8", 'Connection': 'close'}

        data = {  # 获取印章设备信息
            "appKey": appKey,  # 应用标识，接入的应用系统身份标识,由印管平台提供
            "apiKey": "YXYG03_05",  # 接口标识，详细接口标识请参见接口标识
            "timestamp": timestamp_milliseconds,  # 时间戳，本次请求时间戳,单位:毫秒值
            "bizId": '2d23a78864ca4344976fa848594c27bb',  # 业务标识，本次请求业务标识,推荐使用UUID.randomUUID().toString()
            "tenant": tenant,  # 租户标识，由印管平台提供
            "params": "{'uuid':'0X1121SPK234903V00001281','pageNum':1,'pageSize':10}"  # 应用标识
        }
        response = requests.post(url, data=json.dumps(data), headers=headers)  # 定义以JSON格式发送数据
        res = {}
        try:
            if response.status_code == 200:  # 先检查响应状态码
                res = json.loads(response.text)  # 只有状态码为200时才解析JSON
                _logger.info("申请文件类型: {}".format(res))
            else:
                _logger.error(f"请求失败，状态码：{response.status_code}")
        except json.JSONDecodeError as e:
            # 捕获JSON解析错误（如返回内容非JSON格式）
            _logger.error(f"JSON解析失败: {e}, 响应内容：{response.text}")
        except Exception as e:
            # 其他未知异常
            _logger.error(f'申请文件类型报错：{e}')

        try:
            for line in res['data']['list']:
                type_record = type_obj.search([('fileid', '=', line['fileid'])])  # 查有没有相同数据。有，修改；没有，创建。
                pv = {
                    'name': line['name'],
                    'fileid': line['fileid'],
                    'tenant': line['tenant'],
                    'online': line['online'],
                }
                if type_record:
                    type_record.write(pv)
                else:
                    type_obj.create(pv)
        except Exception as e:
            _logger.error(f'{e}')
            return






