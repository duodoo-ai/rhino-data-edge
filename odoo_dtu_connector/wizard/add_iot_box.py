# -*- coding: utf-8 -*-
"""
@Time    : 2025/03/17 16:13
@Author  : Jason Zou
@Email   : zou.jason@qq.com
@Company: zou.jason@qq.com
"""
from odoo import _, api, fields, models
from odoo.exceptions import UserError

TIMEOUT = 20


class AddIotBox(models.TransientModel):
    _inherit= 'add.iot.box'

    imei = fields.Char(string='IMEI')   # 序列号(IMEI)，设备唯一标识码

    def register_dtu_box(self):
        """Register DUT devices"""
        iot_box_obj = self.env['iot.box']
        iot_device_obj = self.env['iot.device']
        if not self.imei:
            raise UserError(_("Please enter a DTU IMEI."))
        device_id = {
            'name': "DTU",
            'imei': self.imei,
            'device_ids': [(0, 0, new_related_values)],
        }
        data = {
            'name': "DTU",
            'imei': self.imei,
            'device_ids': [(0, 0, device_datas)],
        }
        iot_box_record = iot_box_obj.search([('name', '=', 'DTU'), ('imei', '=', self.imei)])
        if iot_box_record:
            raise UserError(_("DTU IMEI Already Exists."))
        else:
            iot_box_obj.create(data)