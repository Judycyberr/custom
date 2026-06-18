from odoo import fields,models

class Users(models.Model):
    _name = 'users'
    _inherit = 'res.users'
    property_id = fields.One2many('estate.property', 'property_type_id')
    users=fields.Char(string='New Field')