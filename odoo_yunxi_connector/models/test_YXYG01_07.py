#!/usr/bin/python
# -*- coding:GBK -*-
import json, requests
import logging
import time
import uuid
_logger = logging.getLogger(__name__)

appKey = 'ZYRGroup'   # Ӧ�ñ�ʶ
# appSecret = '3PUQ4u5w3AQg38OC'  # Ӧ����Կ
tenant = 'zyrg'  # �⻧��ʶ
# ���� UUID
unique_id = uuid.uuid4()
unique_id_str = str(unique_id)
# ��ȡ��ǰʱ��ĺ��뼶ʱ���
timestamp_milliseconds = int(time.time() * 1000)

url = 'http://58.222.101.110:18585/stamper/apis/business/docking/execute'   # ��Ȩ����
headers = {"Content-Type": "application/json; charset=UTF-8", 'Connection': 'close'}

data = {    # �Խ�Ӧ�÷���������֯��������ͬ����ӡ��ƽ̨��
    "appKey": appKey,   # Ӧ�ñ�ʶ�������Ӧ��ϵͳ��ݱ�ʶ,��ӡ��ƽ̨�ṩ
    "apiKey": "YXYG01_07",   # �ӿڱ�ʶ����ϸ�ӿڱ�ʶ��μ��ӿڱ�ʶ
    "timestamp": timestamp_milliseconds,   # ʱ�������������ʱ���,��λ:����ֵ
    "bizId": '2d23a78864ca4344976fa848594c27bb',  # ҵ���ʶ����������ҵ���ʶ,�Ƽ�ʹ��UUID.randomUUID().toString()
    "tenant": "zyrg",  # �⻧��ʶ���⻧��ʶ����ӡ��ƽ̨�ṩ
    "params": "[{'id':'1','name':'�����ܹ�˾','parentId':null,'type':1},{'id':'2','name':'�����ֹ�˾','parentId':'1','type':1},{'id':'21','name':'����','parentId':'2','type':0}]"
}
print(data)
response = requests.post(url, data=json.dumps(data), headers=headers)  # ������JSON��ʽ��������
res = json.loads(response.text)
print(res)



# {
# 	'appKey': 'ZYRGroup',
# 	'apiKey': 'YXYG01_07',
# 	'timestamp': 1739513521440,
# 	'bizId': '2d23a78864ca4344976fa848594c27bb',
# 	'tenant': 'zyrg',
# 	'params': "[{'id':'1','name':'�����ܹ�˾','parentId':null,'type':1},{'id':'2','name':'�����ֹ�˾','parentId':'1','type':1},{'id':'21','name':'����','parentId':'2','type':0}]"
# }