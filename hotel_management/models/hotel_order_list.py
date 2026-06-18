# -*- coding: utf-8 -*-
from openpyxl.worksheet import related

from odoo import fields, models, api


class HotelOrderList(models.Model):
    """All the fields related to Hotel Order List """
    _name = "hotel.order.list"
    _description = "Hotel Order List"

    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    name = fields.Char(string="Name")
    description = fields.Text(string="Description")
    quantity = fields.Integer(string="Quantity", default=1)
    price = fields.Float(string="Price")
    sub_total_price = fields.Integer(string="Sub Total", default=0)
    total_price = fields.Float(string="Total Price", default=0)

    order_id = fields.Many2one('hotel.order.food', string="Order", store=True, ondelete="cascade")
    accommodation_id = fields.Many2one(related='order_id.accommodation_id', string="Accommodations", ondelete="cascade")
    list_total = fields.Float(string="List Total", default=0, compute="_compute_list_total")

    @api.depends('price', 'quantity')
    def _compute_list_total(self):
        """Calculate the total with price and quantity"""
        sum = 0
        for rec in self:
            sum = sum + rec.price * rec.quantity
        self.list_total = sum


