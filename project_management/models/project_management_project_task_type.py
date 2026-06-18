# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta

from odoo import fields,models,api


class ProjectManagementProjectTaskType(models.Model):
    """All the fields related to Project Management Project Task Type"""
    _inherit = "project.task.type"

    default_duration = fields.Integer(string="Default Duration")
    task_ids = fields.One2many('project.task','task_type_id',string="Tasks")

    @api.constrains('default_duration')
    def set_stage_deadline(self):
        """To set the dead-line of the all the task in a stage"""
        for record in self.task_ids:
            record.date_deadline = fields.Datetime.now() + relativedelta(days=self.default_duration)


