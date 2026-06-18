# -*- coding: utf-8 -*-

from odoo import fields,models,api

class PriceList(models.Model):
    _name = "price.list"


    country = fields.Many2one("res.country")

    price_list_id = fields.Many2one(comodel_name='product.pricelist', string="Pricelist")

