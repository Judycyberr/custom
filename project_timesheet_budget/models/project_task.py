# -*- coding: utf-8 -*-

from odoo import fields,models,api

class ProjectTask(models.Model):
    _inherit = "project.task"

    # timesheet_ids = fields.One2many('account.analytic.line','task_id',string="Timesheet IDs")
    # total_time_sheet = fields.Float(string="Total Time Sheet")
    total_net = fields.Float(string="Total Amount", compute="compute_total_exp")
    # project_id = fields.Many2one('project.project',string="Project")

    @api.depends("timesheet_ids")
    def compute_total_exp(self):
        print("task compute is working")
        for record in self:
            if record.timesheet_ids:
                for rec in record.timesheet_ids:
                    record.total_net = record.total_net + rec.total_time_sheet
                    print("Task total",record.total_net)
            else:
                record.total_net = 0










