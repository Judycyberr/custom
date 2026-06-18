# -*- coding: utf-8 -*-

from odoo import fields,models,api


class HotelFoodItems(models.Model):
    """All the fields related to Food Items"""
    _name = "hotel.food.items"

    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    image = fields.Image(string="Image")
    name = fields.Char(string="Name", required=True)
    item = fields.Char(string="Item")
    category_id = fields.Many2one('hotel.food.category', store=True, required=True)
    price = fields.Float(string="Price", required=True)
    description = fields.Text(string="Description")

    def action_open_item_wizard(self):
        """To return the wizard"""
        return {
            "type": "ir.actions.act_window",
            "name": "Food Item",
            "res_model": "hotel.food.items.wizard",
            "view_mode": "form",
            "view_type": "form",
            "context": {
                "default_category_id":self.category_id.id,
                "default_name":self.name,
                "default_price":self.price,
                "default_description":self.description,
                "default_image":self.image,
                "default_item":self.item,
            },
            "target": "new",
        }
    def create_food_product(self):
        """create the same product in lunch"""
        for record in self:
            print("create food product working")
            category = record.category_id
            self.env['lunch.product'].create({
                'name': self.name,
                'category_id': category.id,
                'supplier_id': self.company_id.id,
                'price': self.price,
            })