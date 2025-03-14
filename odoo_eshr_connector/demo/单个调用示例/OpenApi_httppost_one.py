# -*- coding: UTF-8 -*-
import requests
import hashlib
import hmac
import base64
import time
import datetime
import uuid 
#Step1：配置host地址、端口号、appKey和appSecret
# api config
host ='https://10.33.40.117'
port ='443'
artemis='artemis'
api ='/api/resource/v1/org/advance/orgList'
appKey = '22164000'
appSecret = 'DQVK5hB0pbPKEGE1mg4f'
methon = 'POST'

# Step2：组装POST请求URL
# Setting Url
url = host +':' + port +'/' +  artemis  +  api 
print('requesturl:'+ url)

# Step3：组装Headers
# Timestamp
t = time.time()
nowTime = lambda:int(round(t * 1000))
timestamp=nowTime()
timestamp=str(timestamp)
# uuid
nonce= str(uuid.uuid1())

# signature
message = str(methon+'\n*/*\napplication/json\nx-ca-key:'+appKey+'\nx-ca-nonce:'+nonce+'\nx-ca-timestamp:'+timestamp+'\n/'+artemis+api).encode('utf-8')
signature = base64.b64encode(hmac.new(appSecret.encode('utf-8'), message, digestmod=hashlib.sha256).digest())
print(signature)

# Setting Headers
header_dict = dict()
header_dict['Accept'] = '*/*'
header_dict['Content-Type'] = 'application/json'
header_dict['X-Ca-Key'] = appKey
header_dict['X-Ca-timestamp'] = timestamp
header_dict['X-Ca-nonce'] = nonce
header_dict['X-Ca-Signature'] =signature
header_dict['X-Ca-Signature-Headers'] = 'x-ca-key,x-ca-nonce,x-ca-timestamp'

print (header_dict)
 
# Step5：组装传入的Json
# Setting JSON Body
payload = { "pageNo": 1, "pageSize": 1000 }
print(payload)

# Step6：发起POST请求
# Make the requests
r = requests.post(url, headers=header_dict, json=payload,verify=False)

#Step7：解析请求响应
# Check the response
print(r.status_code)
print(r.content.decode('utf-8'))
