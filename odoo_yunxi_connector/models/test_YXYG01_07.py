#!/usr/bin/python
# -*- coding:GBK -*-
import json, requests
import logging
import time
import uuid
_logger = logging.getLogger(__name__)

appKey = 'ZYRGroup'   # 应用标识
# appSecret = '3PUQ4u5w3AQg38OC'  # 应用秘钥
tenant = 'zyrg'  # 租户标识
# 生成 UUID
unique_id = uuid.uuid4()
unique_id_str = str(unique_id)
# 获取当前时间的毫秒级时间戳
timestamp_milliseconds = int(time.time() * 1000)

url = 'http://58.222.101.110:18585/stamper/apis/business/docking/execute'   # 授权处理
headers = {"Content-Type": "application/json; charset=UTF-8", 'Connection': 'close'}

data = {    # 对接应用方主动将组织数据增量同步到印管平台中
    "appKey": appKey,   # 应用标识，接入的应用系统身份标识,由印管平台提供
    "apiKey": "YXYG01_07",   # 接口标识，详细接口标识请参见接口标识
    "timestamp": timestamp_milliseconds,   # 时间戳，本次请求时间戳,单位:毫秒值
    "bizId": '2d23a78864ca4344976fa848594c27bb',  # 业务标识，本次请求业务标识,推荐使用UUID.randomUUID().toString()
    "tenant": "zyrg",  # 租户标识，租户标识，由印管平台提供
    "params": "[{'id':'1','name':'集团总公司','parentId':null,'type':1},{'id':'2','name':'北京分公司','parentId':'1','type':1},{'id':'21','name':'财务部','parentId':'2','type':0}]"
}
print(data)
response = requests.post(url, data=json.dumps(data), headers=headers)  # 定义以JSON格式发送数据
res = json.loads(response.text)
print(res)



# {
# 	'appKey': 'ZYRGroup',
# 	'apiKey': 'YXYG01_07',
# 	'timestamp': 1739513521440,
# 	'bizId': '2d23a78864ca4344976fa848594c27bb',
# 	'tenant': 'zyrg',
# 	'params': "[{'id':'1','name':'集团总公司','parentId':null,'type':1},{'id':'2','name':'北京分公司','parentId':'1','type':1},{'id':'21','name':'财务部','parentId':'2','type':0}]"
# }