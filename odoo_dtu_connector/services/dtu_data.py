# -*- coding: utf-8 -*-
"""
@Time    : 2025/02/27 08:50
@Author  : Jason Zou
@Email   : zou.jason@qq.com
"""
from odoo import models, fields, api

class DtuData(models.Model):
    _inherit = 'dtu.data'

    # 每月流量统计
    monthly_traffic = fields.Float(
        string='Monthly Traffic',
        compute='_compute_monthly_traffic',
        store=False
    )

    # 每季度流量统计
    quarterly_traffic = fields.Float(
        string='Quarterly Traffic',
        compute='_compute_quarterly_traffic',
        store=False
    )

    # 每年流量统计
    yearly_traffic = fields.Float(
        string='Yearly Traffic',
        compute='_compute_yearly_traffic',
        store=False
    )

    # 总流量统计
    total_traffic = fields.Float(
        string='Total Traffic',
        compute='_compute_total_traffic',
        store=False
    )

    @api.depends('time', 'traffic')
    def _compute_monthly_traffic(self):
        aggregate_obj = self.env['dtu.data.aggregate']
        aggregate_record = aggregate_obj.search([('name', '=', '流量统计')])
        for record in self:
            if record.time:
                start_date = fields.Date.from_string(record.time).replace(day=1)
                end_date = start_date.replace(
                    month=start_date.month + 1) if start_date.month < 12 else start_date.replace(
                    year=start_date.year + 1, month=1)
                monthly_records = self.search([
                    ('time', '>=', fields.Datetime.to_string(start_date)),
                    ('time', '<', fields.Datetime.to_string(end_date))
                ])
                record.monthly_traffic = sum(monthly_records.mapped('traffic'))
                aggregate_record.write({'monthly_traffic': sum(monthly_records.mapped('traffic'))})
            else:
                record.monthly_traffic = 0

    @api.depends('time', 'traffic')
    def _compute_quarterly_traffic(self):
        aggregate_obj = self.env['dtu.data.aggregate']
        aggregate_record = aggregate_obj.search([('name', '=', '流量统计')])
        for record in self:
            if record.time:
                date = fields.Date.from_string(record.time)
                quarter_start_month = ((date.month - 1) // 3) * 3 + 1
                start_date = date.replace(month=quarter_start_month, day=1)
                end_date = start_date.replace(
                    month=start_date.month + 3) if start_date.month < 10 else start_date.replace(
                    year=start_date.year + 1, month=1)
                quarterly_records = self.search([
                    ('time', '>=', fields.Datetime.to_string(start_date)),
                    ('time', '<', fields.Datetime.to_string(end_date))
                ])
                record.quarterly_traffic = sum(quarterly_records.mapped('traffic'))
                aggregate_record.write({'quarterly_traffic': sum(quarterly_records.mapped('traffic'))})
            else:
                record.quarterly_traffic = 0

    @api.depends('time', 'traffic')
    def _compute_yearly_traffic(self):
        aggregate_obj = self.env['dtu.data.aggregate']
        aggregate_record = aggregate_obj.search([('name', '=', '流量统计')])
        for record in self:
            if record.time:
                start_date = fields.Date.from_string(record.time).replace(month=1, day=1)
                end_date = start_date.replace(year=start_date.year + 1)
                yearly_records = self.search([
                    ('time', '>=', fields.Datetime.to_string(start_date)),
                    ('time', '<', fields.Datetime.to_string(end_date))
                ])
                record.yearly_traffic = sum(yearly_records.mapped('traffic'))
                aggregate_record.write({'yearly_traffic': sum(yearly_records.mapped('traffic'))})
            else:
                record.yearly_traffic = 0

    @api.depends('traffic')
    def _compute_total_traffic(self):
        aggregate_obj = self.env['dtu.data.aggregate']
        aggregate_record = aggregate_obj.search([('name', '=', '流量统计')])
        for record in self:
            all_records = self.search([])
            record.total_traffic = sum(all_records.mapped('traffic'))
            aggregate_record.write({'total_traffic': sum(all_records.mapped('traffic'))})


