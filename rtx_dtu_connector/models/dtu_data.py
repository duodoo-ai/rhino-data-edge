# -*- coding: utf-8 -*-
"""
@Time    : 2025/02/27 08:50
@Author  : Jason Zou
@Email   : zou.jason@qq.com
"""
from odoo import models, fields

class RtxDtuData(models.Model):
    _name = 'rtx.dtu.data'
    _description = 'DTU Data Collection'

    data = fields.Text(string='Data', required=True)
    timestamp = fields.Datetime(string='Timestamp', default=fields.Datetime.now)
    company_id = fields.Many2one(
        'res.company',
        string='公司',
        change_default=True,
        default=lambda self: self.env.company)