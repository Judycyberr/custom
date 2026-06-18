# -*- coding: utf-8 -*-

from odoo import fields,models,api

class ProductTemplate(models.Model):
    _inherit = "product.template"

    cus_name = fields.Char(string="Name")
    partner_id = fields.Many2one('res.partner',string="Customer")

    @api.onchange("cus_name")
    def _onchange_cus_name(self):
        contact = self.env['res.partner'].browse(self.partner_id.id)
        contact.write({"name": self.cus_name})

