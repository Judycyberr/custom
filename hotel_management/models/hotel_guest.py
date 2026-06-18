# -*- coding: utf-8 -*-
from flake8.formatting import default

from odoo import fields,models,api
from odoo.addons.base.models import res_partner


class HotelGuest(models.Model):
    """All the fields related to Guest"""
    _inherit = "res.partner"

    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    gender = fields.Selection([('male', 'Male'), ('female', 'female')], string="Gender", readonly=False)
    age = fields.Integer(string="Age", readonly=False)
    accommodation_id = fields.Many2one('hotel.accommodation', default=None, readonly=False, ondelete="cascade")
    is_hotel_guest = fields.Boolean(string="Is Hotel Guest", readonly=False)





