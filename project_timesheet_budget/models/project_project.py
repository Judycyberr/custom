# -*- coding: utf-8 -*-
from astroid.raw_building import build_function

from odoo import fields,models,api


class ProjectProject(models.Model):
    _inherit = "project.project"

    budget = fields.Monetary(string="Budget")
    total_exp = fields.Monetary(string="Total Exp", compute="_compute_total_exp")
    # task_ids = fields.One2many('project.task','project_id',string="Tasks")

    def _compute_total_exp(self):
        tasks = self.env['project.task'].search([('project_id','=',self.id)])
        print('*'*20,tasks)
        if tasks:
            for rec in tasks:
                self.total_exp = self.total_exp + rec.total_net
        else:
            self.total_exp = 0
        # self.total_exp = 0


    # @api.depends("task_ids")
    # def _compute_total_exp(self):
    #     for record in self:
    #         if record.task_ids:
    #             for rec in record.task_ids:
    #                 print('each task total amount', rec.mapped('total_net'))
    #                 record.total_exp = record.total_exp + rec.total_net
    #         else:
    #             record.total_exp  = 0
    #
    #         print('budget',record.budget - record.budget * 0.2)
    #         limit = record.budget - record.budget * 0.2
    #         if record.total_exp >= limit:
    #             print("limit reached")
    #             record.message_post(body=("Budget Reached"))











