# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import secrets

from odoo import api, fields, models


# ----------------------------------------------------------
# Models for client
# ----------------------------------------------------------
class IotBox(models.Model):
    _inherit = 'iot.box'

    imei = fields.Char(string='IMEI')   # 序列号(IMEI)，设备唯一标识码
