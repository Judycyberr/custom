# -*- coding: utf-8 -*-
from odoo import fields,models,api


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    total_time_sheet = fields.Float(string="Total Time Sheet", compute="compute_total_time_sheet")
    # task_id = fields.Many2one(string="Task")

    @api.depends('task_id')
    def compute_total_time_sheet(self):
        print("compute is working")
        # for record in self.task_id.timesheet_ids:
        #     print(record.unit_amount)
        #     # print("employee details", self.employee_id)
        #     for rec in self.employee_id:
        #         employee = rec.env['hr.employee'].browse(rec.id)
        #         print("employee name :", employee.name)
        #         print("employee time: ", record.unit_amount)
        #         print("employee money:", employee.hourly_cost)
        #         record.total_time_sheet = record.unit_amount * employee.hourly_cost
        #         print(record.total_time_sheet)

        for rec in self:
            print("time spent : ",rec.unit_amount)
            print("employee name :", rec.employee_id.name)
            rec.total_time_sheet = rec.unit_amount * rec.employee_id.hourly_cost




        print("employee : ",self.employee_id)
        # print(self.env['hr.employee'].browse(self.employee_id.id).hourly_cost)

