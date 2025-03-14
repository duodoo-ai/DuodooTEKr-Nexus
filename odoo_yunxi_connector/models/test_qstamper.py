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
        """��ȡAPI��������"""
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
            # ����������Ч��3600�룬ʵ�ʸ��ݽӿڷ��ص���
            self.token_expire = int(time.time()) + 3600 - 300  # ��ǰ5���ӹ���
        else:
            raise Exception(f"��ȡTokenʧ�ܣ�{response.text}")

    def _ensure_valid_token(self):
        """ȷ������������Ч"""
        if not self.access_token or time.time() >= self.token_expire:
            self._get_access_token()

    def get_authorization_code(self, apply_id, user_info):
        """
    ��ȡ���뵥��Ȩ��
    :param apply_id: ���뵥ID
    :param user_info: �û���Ϣ�ֵ䣬���ٰ���user_id�ֶ�
    :return: ��Ȩ��
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
            "redirectUri": "https://your-callback-url.com/auth",  # �滻Ϊʵ�ʻص���ַ
            "clientId": self.client_id,
            "timestamp": int(time.time() * 1000)
        }

        response = requests.post(auth_url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()['auth_code']
        else:
            raise Exception(f"��ȡ��Ȩ��ʧ�ܣ�{response.text}")


# ʹ��ʾ��
if __name__ == "__main__":
    # ��ʼ���ͻ���
    client = YunxiAuthClient(
        client_id="YOUR_CLIENT_ID",
        client_secret="YOUR_CLIENT_SECRET",
        api_base="https://api.yunxiplatform.com"
    )

    try:
        # �������뵥ID���û���Ϣ
        auth_code = client.get_authorization_code(
            apply_id="APPLY_123456",
            user_info={"user_id": "USER_001"}
        )
        print(f"��ȡ������Ȩ�룺{auth_code}")
    except Exception as e:
        print(f"����ʧ�ܣ�{str(e)}")