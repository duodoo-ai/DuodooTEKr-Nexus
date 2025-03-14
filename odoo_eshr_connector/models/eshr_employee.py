# -*- coding: utf-8 -*-
"""
@Time    : 2024/11/26 10:26
@Author  : Jason Zou
@Email   : zou.jason@qq.com
@Company: 中裕软管科技股份有限公司
"""
import logging
import pymssql
import time
from .conn import *
from odoo import fields, models, api
_logger = logging.getLogger(__name__)


class HikvisionPersonList(models.Model):
    _inherit = 'hikvision.person.list'

    def shr_to_hikvision(self):
        """组织职工信息同步任务  完成SHR同步、 海康平台更新、 职工向海康新增 三个动作"""
        self.action_gen_person_from_shr()   # 从SHR拿待同步记录集
        time.sleep(2)
        self.action_person_list()  # 从海康平台更新中间平台的海康人员ID
        time.sleep(2)
        self.action_person_batch_add()  # 从中间平台批量向海康平台同步增加人员
        time.sleep(2)
        self.action_person_batch_useStatus()  # 从中间平台批量向海康平台同步冻结人员

    @api.model
    def get_model_id(self):
        model_id = self.env['ir.model'].search([('model', '=', self._name)]).id
        return model_id

    def create_server_success_log(self, msg, args1, args2, args3):
        log_obj = self.env['server.log']
        log_obj.create({'model_id': self.get_model_id(),
                        'name': '[%s]-[%s]-[%s]-[%s]' % (msg, args1, args2, args3)})
        _logger.info("-1 [%s]-[%s]-[%s]-[%s]" % (msg, args1, args2, args3))

    def create_server_failures_log(self, msg, args1, args2, args3):
        log_obj = self.env['server.log']
        log_obj.create({'model_id': self.get_model_id(),
                        'name': '[%s]-[%s]-[%s]-[%s]' % (msg, args1, args2, args3)})
        _logger.info("-2 [%s]-[%s]-[%s]-[%s]" % (msg, args1, args2, args3))

    def action_gen_person_from_shr(self):
        try:
            ms_conn = pymssql.connect(
                host="%s" % host,
                user="%s" % user,
                password="%s" % password,
                database="%s" % database,
                charset="utf8")
            shr_cursor = ms_conn.cursor()  # 输出从SHR拿回来的记录集
        except Exception as e:
            _logger.error('连接金蝶SHR数据库失败，请检查网络连接是否正常! 更多可能是你的网络已断开连接！'
                          '==> 连接目标地址：{} '
                          '==> 错误详情：{} '
                          .format(host, e))
            return
        sql = """
            select t.*, thpp.FImageData from (
                SELECT
                    distinct ps.fid as FPersonID,
                    ps.fnumber 职工编码,
                    ps.fname_l2 真实姓名,
                    ps.FIDCardNO 身份证号,
                    ad.fid 部门ID,
                    ad.fnumber 部门编码,
                    ad.fname_l2 部门名称,
                    ps.fcell 手机号,
                    ps.FBirthday 出生日期,
                    pm.FBeginDate 入司日期,
                    ps.FGender 性别,
                    cpos.fname_l2 职位,
                    pt.fname_l2 状态,
                    ad.fparentid 上级部门编码,
                    ps.FFullNamePingYin 拼音
                FROM
                    t_BD_person ps	
                LEFT JOIN T_HR_BDEmployeeType pt on pt.fid = ps.femployeetypeid
                LEFT JOIN t_Org_Positionmember pm ON pm.fpersonid = ps.fid AND pm.fisprimary = 1
                LEFT JOIN t_org_position cpos ON cpos.fid = pm.fpositionid
                LEFT JOIN t_Org_Positionhierarchy ph ON ph.fchildid = cpos.fid
                left join t_org_admin ad on ad.fid = cpos.fadminorgunitid
                LEFT JOIN t_Org_Position ppos ON ppos.fid = ph.fparentid
                LEFT JOIN t_org_positionmember ppm ON ppm.fpositionid = ppos.fid
                LEFT JOIN t_bd_person pps ON pps.fid = ppm.fpersonid
                LEFT JOIN t_ORG_admin PAD ON pad.fid = ad.fparentid
                WHERE PS.FID IS NOT NULL 
                ) t
                LEFT JOIN T_HR_PersonPhoto thpp ON thpp.FPersonID = t.fpersonid 
                ORDER BY 部门编码, 职工编码
        """
        shr_cursor.execute(sql)
        shr_records = shr_cursor.fetchall()
        org_obj = self.env['hikvision.org.list']
        person_obj = self.env['hikvision.person.list']
        if len(shr_records) > 0:
            for line in shr_records:    # 遍历写入数据
                # 写入职工数据
                person_record = person_obj.search([('FPersonID', '=', line[0])])
                dept_id = org_obj.search([('orgIndexCode', '=', line[4])])
                pv = {
                    'FPersonID': line[0],
                    'jobNo': line[1],
                    'name': line[2],
                    'FIDCardNO': line[3] or False,
                    'dept_fid': dept_id.id or False,
                    'dept_code': dept_id.orgNo or False,
                    'dept_name': dept_id.name or False,
                    'fcell': line[7] or False,
                    'FBirthday': line[8] or False,
                    'FBeginDate': line[9] or False,
                    'FGender': str(line[10]) or False,
                    'position': line[11] or False,
                    'EmployeeType': line[12] or False,
                    'pinyin': line[14] or False,
                    'wo_person_picture_attachment': line[15] or False,
                    'SyncState': 0,
                    }
                if person_record:
                    person_record.write(pv)
                else:
                    person_obj.create(pv)
