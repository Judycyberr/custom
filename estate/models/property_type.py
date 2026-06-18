from odoo import fields,models

class PropertyType(models.Model):
    _name='property.type'
    _description='Estate Property Type'
    name=fields.Char(required=True)
    property_id=fields.One2many('estate.property','property_type_id')

    _name_uniq = models.Constraint(
        'unique (name)',
        'Type name already exists!',
    )