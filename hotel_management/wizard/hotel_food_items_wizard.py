# -*- coding: utf-8 -*-

from odoo import fields,models


class HotelFoodItemsWizard(models.TransientModel):
    """All the fields related to Food Items Wizard"""
    _name = "hotel.food.items.wizard"

    image = fields.Image(string="Image")
    name = fields.Char(string="Name")
    item = fields.Char(string="Item")
    category_id = fields.Many2one('hotel.food.category')
    price = fields.Float(string="Price")
    description = fields.Text(string="Description")
    food_order_ids =fields.One2many('hotel.order.food','item_ids',string="Orders")

    def add_to_list(self):
        """Add items to list"""
        exist = self.env['hotel.order.list'].search([
            ('name', '=', self.name),
            ('order_id', '=', self.env.context.get("order_id"))])

        if (exist):
            for record in exist:
                record.quantity = record.quantity+1
        else:
            self.env['hotel.order.list'].create({
                 'name': self.name,
                'price': self.price,
                'order_id': self.env.context.get("order_id"),
            })