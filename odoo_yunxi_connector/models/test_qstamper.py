import requests
import json
import time


class YunxiAuthClient:
    def __init__(self, client_id, client_secret, api_base):
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_base = api_base
        self.access_token = None
        self.token_expire = 0

    def _get_access_token(self):
        """获取API访问令牌"""
        token_url = f"{self.api_base}/oauth/token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }
        response = requests.post(token_url, data=data)
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data['access_token']
            # 假设令牌有效期3600秒，实际根据接口返回调整
            self.token_expire = int(time.time()) + 3600 - 300  # 提前5分钟过期
        else:
            raise Exception(f"获取Token失败：{response.text}")

    def _ensure_valid_token(self):
        """确保访问令牌有效"""
        if not self.access_token or time.time() >= self.token_expire:
            self._get_access_token()

    def get_authorization_code(self, apply_id, user_info):
        """
    获取申请单授权码
    :param apply_id: 申请单ID
    :param user_info: 用户信息字典，至少包含user_id字段
    :return: 授权码
    """
        self._ensure_valid_token()

        auth_url = f"{self.api_base}/api/v1/authorization/code"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "applyId": apply_id,
            "userId": user_info['user_id'],
            "redirectUri": "https://your-callback-url.com/auth",  # 替换为实际回调地址
            "clientId": self.client_id,
            "timestamp": int(time.time() * 1000)
        }

        response = requests.post(auth_url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()['auth_code']
        else:
            raise Exception(f"获取授权码失败：{response.text}")


# 使用示例
if __name__ == "__main__":
    # 初始化客户端
    client = YunxiAuthClient(
        client_id="YOUR_CLIENT_ID",
        client_secret="YOUR_CLIENT_SECRET",
        api_base="https://api.yunxiplatform.com"
    )

    try:
        # 假设申请单ID和用户信息
        auth_code = client.get_authorization_code(
            apply_id="APPLY_123456",
            user_info={"user_id": "USER_001"}
        )
        print(f"获取到的授权码：{auth_code}")
    except Exception as e:
        print(f"操作失败：{str(e)}")