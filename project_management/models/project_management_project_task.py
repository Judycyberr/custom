# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta

from odoo import fields,models,api

class ProjectManagementProjectTask(models.Model):
    """All fields related to ProjectManagementProjectTask"""
    _inherit = "project.task"

    task_type_id = fields.Many2one('project.task.type',string='Task Type')

    @api.constrains('stage_id')
    def set_date_deadline(self):
        """passing the date deadline"""
        self.task_type_id = self.stage_id
        self.date_deadline = fields.Datetime.now() + relativedelta(days=self.task_type_id.default_duration)