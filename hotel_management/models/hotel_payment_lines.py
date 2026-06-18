# -*- coding: utf-8 -*-

from odoo import fields, models

class HotelPaymentLines(models.Model):
    """All the fields related to Hotel Payment Line """
    _name = 'hotel.payment.lines'

    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    product_id = fields.Many2one("product.product")
    price = fields.Float(mapped_field = "product_id.lst_price")
    accommodation_id = fields.Many2one('hotel.accommodation')
    order_id = fields.Many2one('hotel.order.food')


