from odoo import fields,models

class RaceInventory(models.Model):
    _inherit = 'stock.warehouse.orderpoint'