from odoo import fields,models

class RaceEvents(models.Model):
    _inherit = "event.event"
    internal_notes=fields.Text(string="Internal Notes")