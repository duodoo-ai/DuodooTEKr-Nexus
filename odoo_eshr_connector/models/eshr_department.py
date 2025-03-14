# -*- coding: utf-8 -*-
"""
@Time    : 2024/12/05 8:20
@Author  : Jason Zou
@Email   : zou.jason@qq.com
@mobile  : 18951631470
"""
import logging
import pymssql
from odoo import fields, models, api
from .eshr_conn import *
_logger = logging.getLogger(__name__)


class EShrDepartment(models.Model):
    _inherit = 'hr.department'
    _description = '金蝶e-shr组织架构同步'

    fid = fields.Char(string='e-shr FID')
    fnum = fields.Char(string='e-shr 部门编码')

    def cron_org_from_shr(self):
        try:
            ms_conn = pymssql.connect(
                host="%s" % host,
                user="%s" % user,
                password="%s" % password,
                database="%s" % database,
                charset="utf8")
            shr_cursor = ms_conn.cursor()  # 输出从SHR拿回来的记录集
        except Exception as e:
            _logger.error('连接金蝶e-shr数据库失败，请检查网络连接是否正常! 更多可能是你的网络已断开连接！'
                          '==> 连接目标地址：{} '
                          '==> 错误详情：{} '
                          .format(host, e))
            return
        sql = """
            SELECT
                fid,
                fname_l2 AS fname,
                fnumber,
                fparentid,
                flevel - 2 
            FROM
                T_ORG_Admin 
            WHERE
                fissealup = 0 
            ORDER BY
                fnumber
        """
        shr_cursor.execute(sql)
        shr_records = shr_cursor.fetchall()
        org_obj = self.env['hr.department']
        if len(shr_records) > 0:
            for line in shr_records:    # 遍历写入数据
                # 写入组织数据
                org_record = org_obj.search([('orgIndexCode', '=', line[0])])
                dept_id = org_obj.search([('orgIndexCode', '=', line[3])])
                uv = {
                    'orgIndexCode': line[0],  # 组织唯一标识码
                    'name': line[1] or False,
                    'orgNo': line[2] or False,
                    'parentOrgIndexCode': line[3] or False,
                    'parent_id': dept_id and dept_id[0].id or False,
                    'SyncState': 0,
                }
                if org_record:
                    org_record.write(uv)
                else:
                    org_obj.create(uv)
