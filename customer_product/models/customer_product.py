# -*- coding: utf-8 -*-

from odoo import fields,models,api


class CustomerProduct(models.Model):
    _inherit = "res.partner"

    is_product = fields.Boolean(string="Is Product")


    # @api.constrains("is_product")
    # def _check_is_product(self):
    #     print("function is working")
    #     if self.is_product:
    #         self.env['product.template'].create({'name':self.name})
    #         print("create is working")

    # def default_get(self, fields):
    #     print("function is working")

    @api.model
    def create(self, values):
        res = super().create(values)
        for rec in values:
            print("record",rec)
            if rec.get("is_product"):
                self.env['product.template'].create({'name':rec.get("name"),'cus_name':rec.get("name"),'partner_id':res.id})
                print("product created")
        print("res",res.id)
        return res

    @api.model
    def write(self, values):
        print("values",values)
        res = super().write(values)
        print("res",self.id)
        product = self.env['product.template'].search([('partner_id','=',self.id)])
        print("product",product)
        product.write({'name':values.get("name")})
        return res


