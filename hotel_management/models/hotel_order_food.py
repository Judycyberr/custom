# -*- coding: utf-8 -*-
from openpyxl.worksheet import related

from odoo import fields, models, api, service


class HotelOrderFood(models.Model):
    """All the fields related to Order Food """
    _name = 'hotel.order.food'
    _description = 'Hotel Order Food'
    _rec_name = 'room_id'

    accommodation_id = fields.Many2one('hotel.accommodation', string="Accommodation", store=True, ondelete="cascade")
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    room_id = fields.Many2one(related="accommodation_id.room_id", string="Room")
    guest_ids = fields.One2many(related="accommodation_id.guest_ids", string="Guest")
    order_time = fields.Datetime(string="Order Time", default=fields.Datetime.now)
    state = fields.Selection(related="accommodation_id.state", string="State")
    category_ids = fields.Many2many('hotel.food.category', string="Category", store=True)
    item_ids = fields.Many2many('hotel.food.items', string="Item")
    order_quantity = fields.Integer(string="Quantity", readonly=False)
    order_list_ids = fields.One2many("hotel.order.list","order_id", string="Order List", store=True)
    # food_total_price = fields.Float(string="Total Price", compute="_compute_food_total_price")
    item_total = fields.Float(string="Sub Total", related="order_list_ids.list_total", store=True)
    name = fields.Char(string="Name")
    temp = fields.Float(compute="cafe_creation_price_updation")
    service_product_id = fields.Many2one('hotel.payment.lines', string="Service Product")

    @api.onchange('category_ids')
    def onchange_category(self):
        """To get all the food items based on the category"""
        if self.category_ids:
            self.item_ids = self.env['hotel.food.items'].search([('category_id', '=', self.category_ids)])



    @api.depends('order_list_ids')
    def cafe_creation_price_updation(self):
        """update the price of product"""
        sum = 0
        count = 1
        product_1 = self.env.ref('hotel_management.product_1')
        if self.env['hotel.payment.lines'].search([('order_id', 'in', self.ids),('price','>',0)]):
            for rec in self.order_list_ids:
                sum = sum + rec.list_total
                count = count + 1
            if (count > 1):
                price = sum/2
            order = self.env['hotel.payment.lines'].search([('order_id', 'in', self.ids),('product_id', '=',product_1.id)])
            order.write({
                'price':price})
            # order.price = price
        else:
            if self.order_list_ids.list_total > 0:
                self.env['hotel.payment.lines'].create({
                    'product_id': product_1.id,
                    'accommodation_id': self.accommodation_id.id,
                    'order_id': self.id,
                    'price': self.order_list_ids.list_total
                })
        self.temp = 0

