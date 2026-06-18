# -*- coding: utf-8 -*-

from odoo import fields,models,api

class SaleOrderProjectTask(models.Model):
    _inherit = "project.task"
    sale_order_id = fields.Many2one('sale.order')

    def action_view_sale_order(self):
        print("sale_order butoon is being clicked")
        # task = self.env['sale.order'].search([('name','=','butoon')])
        # self.sale_order_id = self.env['sale.order'].search([('id','=',self.sale_order_id.id)])
        print(self.sale_order_id)
        return {
            "name": "Task View",
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'target': 'current',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.sale_order_id.id,
        }