#!/usr/bin/python
# -*- coding:GBK -*-
import json
import logging

from k3cloud_webapi_sdk.main import K3CloudApiSdk
import time
import unittest


# ���ȹ���һ��SDKʵ��
api_sdk = K3CloudApiSdk()

# Ȼ���ʼ��SDK����ָ����ز���������ᵼ��SDK��ʼ��ʧ�ܶ��޷�ʹ�ã�

# ��ʼ������һ��Init��ʼ��������ʹ��conf.ini�����ļ�
# config_path:�����ļ�����Ի����·��������ʹ�þ���·��
# config_node:�����ļ��еĽڵ�����
api_sdk.Init(config_path='../conf.ini', config_node='config')

# ��ʼ������������������InitConfig��ʼ��������ֱ�Ӵ��Σ���ʹ�������ļ�
# acct_id:������ϵͳ��¼��Ȩ������ID,user_name:������ϵͳ��¼��Ȩ���û�,app_id:������ϵͳ��¼��Ȩ��Ӧ��ID,app_sec:������ϵͳ��¼��Ȩ��Ӧ����Կ
# server_url:k3cloud����url(��˽���ƻ�����Ҫ����),lcid:������ϵ(Ĭ��2052),org_num:��֯����(���ö���֯ʱ���ö�Ӧ����֯�������Ч)
# api_sdk.InitConfig('62e25034af8811', 'Administrator', '231784_3d9r4dHJ5OgZ4aUJwe6rTxSMVjTdWooF', 'aae9d547ffde46fe9236fdea40472854')

# �˴������챣��ӿڵĲ����ֶ�����ʾ����ʹ��ʱ��ο�WebAPI����ӿڵ�ʵ�ʲ����б�
current_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
save_data = {
    "FCreateOrgId": {"FNumber": 100},
    "FUserOrgId": {"FNumber": 100},
    "FNumber": "xtwl" + current_time + "10001",
    "FName": "��������" + current_time + "10001"
}
FNumber = "xtwl" + current_time + "10001"


def Check_response(res):
    res = json.loads(res)
    if res["Result"]["ResponseStatus"]["IsSuccess"]:
        return True
    else:
        logging.error(res)
        return False


def material_Save(**kwargs):
    """
    ���ӿ�����ʵ������ (BD_MATERIAL) �ı��湦��
    :param kwargs:  �滻para�в�����ʾ���� Model = {"FCreateOrgId": {"FNumber": 100},"FUserOrgId": {"FNumber": 100},"FNumber": "Webb10001","FName": "��������10001"}
    :return:
    """
    para = {
        "NeedUpDateFields": [],
        "NeedReturnFields": [],
        "IsDeleteEntry": "True",
        "SubSystemId": "",
        "IsVerifyBaseDataField": "False",
        "IsEntryBatchFill": "True",
        "ValidateFlag": "True",
        "NumberSearch": "True",
        "IsAutoAdjustField": "False",
        "InterationFlags": "",
        "IgnoreInterationFlag": "",
        "IsControlPrecision": "False",
        "Model": {}
    }
    if kwargs:
        para.update(kwargs)
    response = api_sdk.Save("BD_Material", para)
    print("���ϱ���ӿڣ�", response)
    if Check_response(response):
        res = json.loads(response)
        materialid = res["Result"]["Id"]
        return Check_response(response), materialid
    return False, ""


def material_Submit(**kwargs):
    """
    ���ӿ�����ʵ������ (BD_MATERIAL) ���ύ����
    :param kwargs:  �滻para�в�����ʾ����   Numbers = []
    :return:
    """
    para = {"CreateOrgId": 0, "Numbers": [], "Ids": "", "SelectedPostId": 0,
            "NetworkCtrl": "",
            "IgnoreInterationFlag": "",
            }
    if kwargs:
        para.update(kwargs)
    response = api_sdk.Submit("BD_Material", para)
    print("�����ύ�ӿڣ�", response)
    return Check_response(response)


def material_Audit(**kwargs):
    """
    ���ӿ�����ʵ������ (BD_MATERIAL) ����˹���
    :param kwargs:  �滻para�в�����ʾ����   Numbers = []
    :return:
    """
    para = {"CreateOrgId": 0, "Numbers": [], "Ids": "", "SelectedPostId": 0,
            "NetworkCtrl": "",
            "IgnoreInterationFlag": "",
            "IsVerifyProcInst": "",
            }
    if kwargs:
        para.update(kwargs)
    response = api_sdk.Audit("BD_Material", para)
    print("������˽ӿڣ�", response)
    return Check_response(response)


def material_FlexSave(**kwargs):
    """
    ���ӿ�����ʵ�ֵ����򱣴湦��
    �������
    :param kwargs:  �滻para�в�����ʾ����
    :return:
    """
    para = {"Model":[{"FFLEX8":{"FNumber": kwargs["FNumber"]}}]}
    response = api_sdk.FlexSave("BD_FLEXITEMDETAILV",para)
    print("�����򱣴�ӿڣ�", response)
    return Check_response(response)


class MaterialTestCase(unittest.TestCase):

    def testa_material_Save(self):
        result = material_Save(Model=save_data)
        self.assertTrue(result[0])

    def testb_material_Submit(self):
        self.assertTrue(material_Submit(Numbers=[FNumber]))

    def testc_material_Audit(self):
        self.assertTrue(material_Audit(Numbers=[FNumber]))

    def testd_material_flexsave(self):
        self.assertTrue(material_FlexSave(FNumber=FNumber))



if __name__ == '__main__':
    unittest.main()
