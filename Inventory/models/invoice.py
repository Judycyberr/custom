# -*- coding: utf-8 -*-
from odoo import fields,models,api
from odoo.exceptions import ValidationError


class Invoice(models.Model):
    _inherit = "account.move"

    stock_picking_id = fields.Many2one('stock.picking',string= "Stock Picking")

    @api.onchange('stock_picking_id')
    def add_product(self):
        print("add_product")
        print(self.invoice_line_ids)
        print(self.stock_picking_id.move_ids.product_id)
        self.invoice_line_ids = None
        print("company", self.company_id.name)
        print("move_id", self.invoice_line_ids.move_id)
        # for rec in self.stock_picking_id.move_ids.product_id:
        #     self.invoice_line_ids.create({
        #         'product_id': rec.id,
        #         'move_id': self.invoice_line_ids.move_id,
        #     })
        #     print("inside for loop")
        # self.env['account.move.line'].create({
        #     "product_id": [fields.Command.link(self.stock_picking_id.move_ids.product_id)],
        #     'move_id': self.invoice_line_ids.move_id,
        # })
        # self.env['account.move'].create({
        #     'invoice_line_ids': [fields.Command.create({
        #         'product_id': self.stock_picking_id.move_ids.product_id.id,
        #     })],
        # })
        # for rec in self.stock_picking_id.move_ids.product_id:
        #     print("records", rec)
        #     self.invoice_line_ids = fields.Command.create({
        #         'product_id': rec.id,
        #         })
        #     self.invoice_line_ids.product_id = rec
        #     print(self.invoice_line_ids.product_id)
        lines = []
        for record in self.stock_picking_id.move_ids:
            lines.append(fields.Command.create({
                'product_id': record.product_id.id,
            }))
            print("lines",lines )
            self.invoice_line_ids = lines

        print("Product in invoice : ",self.invoice_line_ids.product_id)

    def action_post(self):
        res = super(Invoice,self).action_post()
        print("confirmm button")
        # for record in self.invoice_line_ids:
        #     print(record.product_id.name)
        #     print(record.quantity)
        #     if record.quantity <= 0:
        #         raise ValidationError ("Quantity Cannot be 0")

        for record in self.stock_picking_id:
            print(record)

        return res





