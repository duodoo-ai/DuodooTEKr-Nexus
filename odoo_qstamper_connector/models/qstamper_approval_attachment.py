# -*- coding: utf-8 -*-
"""
@Time    : 2025/1/6 8:20
@Author  : Jason Zou
@Email   : zou.jason@qq.com
@mobile  : 18951631470
"""
import json, time, logging
import base64
import binascii
import fitz
from io import BytesIO
from odoo import api, fields, models
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4
from k3cloud_webapi_sdk.main import K3CloudApiSdk
_logger = logging.getLogger(__name__)

# 首先构造一个SDK实例
api_sdk = K3CloudApiSdk()
# config_node:配置文件中的节点名称
api_sdk.Init(config_path='tone_good/sdk/conf.ini', config_node='config')
# 此处仅构造保存接口的部分字段数据示例，使用时请参考WebAPI具体接口的实际参数列表
current_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
# 获取当前本地时间
local_time = time.localtime()
# 将时间元组转换为时间戳
timestamp = time.mktime(local_time)
# 加上指定的小时数（这里是 8 小时）
timestamp += 8 * 3600
# 将新的时间戳转换为时间元组
new_local_time = time.localtime(timestamp)
# 将时间元组格式化为字符串
formatted_time = time.strftime("%Y%m%d%H%M%S", new_local_time)
pic = 'tone_good/interface_qstamper/pic/'


class QstamperApproval(models.Model):
    _inherit = 'qstamper.approval'

    # =============== 判断有附件字段，则拿附件去加受控水印 ===============
    # =============== 判断有附件字段，则拿附件去加受控水印 ===============
    # =============== 判断有附件字段，则拿附件去加受控水印 ===============
    def Search_attachmentDownLoad(self, file_id, bill_id):
        try:
            _logger.info('单据号 {} ----- 附件号 {} 正在进行附件加水印转换'.format(bill_id, file_id))
            attach_size, source_attach_name, source_binary_data, dest_attach_name, dest_attach_data \
                = self.Download_attachmentDownLoad(FileId=file_id, BillId=bill_id)  # 查销售订单
            return attach_size, source_attach_name, source_binary_data, dest_attach_name, dest_attach_data
        except Exception as e:
            # 处理异常情况，记录日志并返回 None
            # _logger.error(f"Search_attachmentDownLoad执行出错 加水印出现异常: {str(e)}，附件 ID: {file_id}，单据号: {bill_id}")
            return None

    def Download_attachmentDownLoad(self, **kwargs):
        """
        本接口用于实现销售订单 (SAL_SaleOrder) 的下载功能
        输入参数
        :param kwargs:  替换para中参数，示例：   Numbers = []
        :return:
        """
        watermark_file = pic + "watermark.png"   # 指定的水印文件路径
        output_pdf = pic + "output.pdf"   # 指定的水印文件路径
        para = {
            "FileId": "",
            "StartIndex": 0
        }
        if kwargs:
            para.update(kwargs)
        response = api_sdk.attachmentDownLoad(para)
        try:
            res = json.loads(response)
            attach_size = res['Result']['FileSize']
            source_attach_name = res['Result']['FileName']
            source_binary_data = res['Result']['FilePart']  # PDF二进制数据
            # 解码Base64字符串为二进制数据
            # 注意：
            # 1、source_binary_data 没有编码可以存入 PGSQL 数据库；
            # 2、base64.b64encode 编码可以存入 PGSQL 数据库；
            # base64.b64encode(source_binary_data) 将原始二进制数据编码为 Base64 编码的字符串
            # base64.b64decode(encoded_data) 将 Base64 编码的数据解码为原始二进制数据
            encoded_binary_data = base64.b64decode(source_binary_data)
            # 检查是否是PDF文件的二进制数据（PDF文件通常以%PDF-开头）
            if not encoded_binary_data.startswith(b'%PDF-'):
                _logger.info(f"Download_attachmentDownLoad执行出错 文件格式不支持: "
                             f"附件 ID: {kwargs['FileId']}，"
                             f"单据号: {kwargs['BillId']}，"
                             f"文件名: {source_attach_name}")
                return None  # 当不是 PDF 时返回 None
        except binascii.Error:
            return None
        try:
            # 去给二进制附件增加“受控”水印
            dest_attach_data = self.add_watermark(encoded_binary_data, output_pdf, watermark_file)
            # 将 Base64 编码的数据解码为原始二进制数据
            dest_attach_data = base64.b64encode(dest_attach_data)
            dest_attach_name = '(已受控)' + source_attach_name
            return attach_size, source_attach_name, source_binary_data, dest_attach_name, dest_attach_data
        except Exception as e:
            _logger.error(f"添加水印时出错: {e}")
            return None

    def repair_pdf(self, input_pdf_binary):
        try:
            # 使用 PyMuPDF 打开并修复 PDF
            doc = fitz.open(stream=input_pdf_binary, filetype="pdf")
            repaired_pdf_binary = BytesIO()
            doc.save(repaired_pdf_binary)
            doc.close()
            repaired_pdf_binary.seek(0)
            return repaired_pdf_binary.read()
        except Exception as e:
            print(f"Error repairing PDF: {e}")
            return input_pdf_binary

    def add_watermark(self, input_pdf_binary, output_pdf, watermark_image, x_position=30, y_position=50, opacity=1):
        # x_position=700, y_position=510, opacity=1
        # 尝试修复 PDF
        repaired_pdf_binary = self.repair_pdf(input_pdf_binary)
        input_pdf_obj = PdfReader(BytesIO(repaired_pdf_binary))  # 从二进制数据中读取 PDF
        output_pdf_obj = PdfWriter()
        output_buffer = BytesIO()

        # 创建一个临时的 PDF 作为水印
        # input_pdf_binary 是输入的 PDF 二进制数据，watermark_image 是水印图像
        # opacity 是透明度，x_position 和 y_position 是水印的位置坐标
        # 设置为横向 A4 页面尺寸，交换宽度和高度
        page_width, page_height = A4[1], A4[0]
        c = canvas.Canvas(output_buffer, pagesize=(page_width, page_height))
        try:
            c.setFillColor(colors.white)  # 将背景设置为白色
            c.setFillColor(colors.red)  # 设置字体颜色为红色
            c.setFont("Helvetica", 12)  # 设置字体和字体大小
            c.setFillAlpha(opacity)  # 设置透明度
            c.setStrokeColor(colors.transparent)  # 设置笔触颜色为透明
            # 读取图像
            img = ImageReader(watermark_image)
            if x_position is not None and y_position is not None:
                # 旋转 20 度
                c.saveState()
                c.translate(x_position, y_position)
                c.rotate(20)
                c.drawImage(img, 0, 0, width=60, height=25)
                c.restoreState()
            else:
                # 修改图像尺寸为 60*25
                x = (page_width - 60) / 2
                y = (page_height - 25) / 2
                c.saveState()
                c.translate(x, y)
                c.rotate(20)
                c.drawImage(img, 0, 0, width=60, height=25)
                c.restoreState()
        except Exception as e:
            raise ValueError(f"Error drawing image: {e}")
        c.showPage()
        c.save()

        # 将水印 PDF 与原始 PDF 合并
        watermark_pdf = PdfReader(output_buffer)
        for page in input_pdf_obj.pages:
            page.merge_page(watermark_pdf.pages[0])
            output_pdf_obj.add_page(page)

        # ====将合并后的 PDF 存储在新的 BytesIO 对象中==================
        final_output_buffer = BytesIO()
        output_pdf_obj.write(final_output_buffer)
        # # 读取二进制数据
        binary_data = final_output_buffer.getvalue()
        # =========================================================

        # ----保存输出 PDF，用以将文件回传到云星空 ---------------------
        with open(output_pdf, 'wb') as f:
            output_pdf_obj.write(f)
        # --------------------------------------------------------
        return binary_data


    # =============== 从ERP查询订单数据 到中间平台 回馈附件给云星空 ===============
    # =============== 从ERP查询订单数据 到中间平台 回馈附件给云星空 ===============
    # =============== 从ERP查询订单数据 到中间平台 回馈附件给云星空 ===============
    def Search_attachmentUpload(self, InterId, BillNO):
        try:
            # 查销售订单附件ID + 销售订单号，去回传附件给云星空
            self.Upload_attachmentUpload(InterId=InterId, BillNO=BillNO)
        except Exception as e:
            _logger.error('受控水印：销售订单 {} 附件回传云星空主方法接口错误: {}'.format(BillNO, e))

    def file_to_base64(self, file_path):
        with open(file_path, 'rb') as f:
            return base64.b64encode(f.read()).decode()

    def Upload_attachmentUpload(self, **kwargs):
        """
        本接口用于实现通用单据附件的上传功能
        输入参数
        :param kwargs:  替换para中参数，示例：   InterId="", BillNO="
        :return:
        """
        file_path = 'tone_good/interface_qstamper/pic/output.pdf'
        encode_binary_data = self.file_to_base64(file_path)
        approval_obj = self.env['qstamper.approval']
        approval_record = approval_obj.search([('name', '=', kwargs['BillNO'])])
        filename = approval_record.dest_binary_data_name
        para = {"FileName": filename,
                "FEntryKey": 0,
                "FormId": 'SAL_SaleOrder',  # 要上传附件的业务对象标识
                "IsLast": True,
                "InterId": kwargs['InterId'],  # 要上传附件的业务对象单据表主键值
                "BillNO": kwargs['BillNO'],     # 单据编号
                "AliasFileName": '加受控时间' + formatted_time + filename,
                "SendByte": encode_binary_data
                }
        if kwargs:
            para.update(kwargs)
        response = api_sdk.attachmentUpload(para)
        try:
            json.loads(response)
        except (ValueError, OverflowError) as e:
            _logger.error(f"JSON解析错误: {e}")
        return False, ""



    # 保存输出 PDF
    # with open(output_pdf, 'wb') as f:
    #     output_pdf_obj.write(f)