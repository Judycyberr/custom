# -*- coding: utf-8 -*-
from odoo import fields,models


class HotelFoodCategory(models.Model):
    """All the fields related to Food Category """
    _name = 'hotel.food.category'

    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    name = fields.Char(string="Name")
    food_item_ids = fields.One2many('hotel.food.items', 'category_id')
    category_order_ids =fields.Many2many('hotel.order.food')
