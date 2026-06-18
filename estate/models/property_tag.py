from odoo import fields,models

class PropertyTag(models.Model):
    _name = 'property.tag'
    _description = 'Property Tag'
    name = fields.Char(required=True)
    property_id = fields.Many2many('estate.property')

    _name_uni= models.Constraint(
        'unique(name)',
        'Tag name already exists'
    )