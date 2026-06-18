# -*- coding: utf-8 -*-

from odoo import fields,models,api

class SaleOrderPriceList(models.Model):
    _inherit = "sale.order"

    price_list_id = fields.Many2one("price.list", string="New Price List")

    def action_confirm(self):
        price_list = self.env["price.list"].search([('country', '=', self.partner_id.country_id)])
        print("test",price_list.country.name)
        # for rec in price_list:
        #     print("Inside loop",rec.country.name)
        #     print("partner counter",self.partner_id.country_id.name)
        #     if rec.country.name == self.partner_id.country_id.name:
        self.pricelist_id = price_list.price_list_id
        res = super(SaleOrderPriceList, self).action_confirm()
        # print("RES",res)
        return res

    # def _compute_pricelist_id(self):
    #     res = super(SaleOrderPriceList,self)._compute_pricelist_id()
    #     print ("compute method overriden")
    #     price_list = self.env["price.list"].search([])
    #     print(price_list.country)
    #     for rec in price_list:
    #         print("Inside loop", rec.country.name)
    #         print("partner counter", self.partner_id.country_id.name)
    #         if rec.country.name == self.partner_id.country_id.name:
    #             self.pricelist_id = rec.price_list_id
    #             print("working")
    #     return res
