# -*- coding: utf-8 -*-

from odoo import fields,models,api
from odoo.exceptions import ValidationError


class SaleOrderTask(models.Model):
    """All fields related to Sale Order Task"""
    _inherit = "sale.order"

    project_id = fields.Many2one("project.project")
    project_ids = fields.Many2many("project.project")
    is_project = fields.Boolean(default=False)
    task_ids = fields.One2many("project.task","sale_order_id")
    subtask_count = fields.Integer()
    flag = fields.Boolean(default=False)
    # @api.onchange('partner_id')
    # def get_project(self):
    #     print("onchange is working")
    #     rec = self.env['project.project'].search([('partner_id', '=', self.partner_id)])
    #     if(self.partner_id):
    #         if rec:
    #             for record in rec:
    #                 self.write({'project_ids':rec})
    #         else:
    #             self.write({'project_ids':None})

    @api.onchange("partner_id")
    def get_project_domain(self):
        if(self.partner_id):
            rec = self.env['project.project'].search([('partner_id', '=', self.partner_id)])
            self.project_ids = rec
        else:
            self.project_ids = False

    @api.constrains("project_id")
    def _check_project_id(self):
        if self.project_id:
            print("Present")
            self.is_project = True
        else:
            print("empty")
            self.is_project = False

    def action_task(self):
        rec = self.env["project.task"].search([('project_id', '=', self.project_id)])
        print(rec)
        check = False
        self.subtask_count = 1
        for record in rec:
            print(record.name)
            print(self.name)
            if self.name in record.name:
                print("Already Exist")
                check = False
                raise ValidationError("Task Already Exists For This Sale Order")
            else:
                check = True

        if check==True:
            self.flag = True
            self.task_ids = self.env["project.task"].create({'name': self.name, 'project_id': self.project_id.id,
                                                    'description': f"The partner is {self.partner_id.name} , payment terms : {self.payment_term_id.name}",
    })
            print("task created")

            sale_order_lines = self.order_line
            for record in sale_order_lines:
                self.subtask_count += 1
                # self.task_ids.quantity = record.product_uom_qty
                self.env['project.task'].create({'parent_id':self.task_ids.id, 'name':f"{record.name} - {record.product_uom_qty}"})
            print('all the task ids',self.task_ids.id)

    def action_view_task(self):
        all_task = self.env['project.task'].search([('name', '=', self.name)]) + self.env['project.task'].search([('parent_id', '=', self.task_ids.ids)])
        for record in all_task:
            record.write({'sale_order_id':self.id})
        view_list = self.env.ref('project.project_task_view_tree_main_base').id
        view_form = self.env.ref('project.view_task_form2').id
        if self.subtask_count >= 1:
            return {
                "name": "Task View",
                'type': 'ir.actions.act_window',
                'res_model': 'project.task',
                'target': 'current',
                'view_mode': 'list,form',
                'view_type': 'list,form',
                # 'view_id': view_list,
                'views': [[view_list, 'list'],
                          [view_form, 'form']],
                'domain': ["|", ("name", "=", self.name), ("parent_id", "in", self.task_ids.ids)]
            }
        else:
            raise ValidationError("Task Not Exist")

    def action_cancel(self):
        res = super(SaleOrderTask,self).action_cancel()
        self.subtask_count = 0
        print("overriden succesfully")
        print(self.id)
        parent_task = self.env['project.task'].search([('name', '=', self.name)])
        # print(self.task_ids)
        print('TAskss',parent_task)
        parent_task.unlink()
        return res

    def action_confirm(self):
        res = super(SaleOrderTask,self).action_confirm()
        self.flag = False
        return res
