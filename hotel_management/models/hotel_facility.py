# -*- coding: utf-8 -*-
from odoo import fields,models


class HotelFacility(models.Model):
    """All the fields related to Hotel Facility"""
    _name = 'hotel.facility'

    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    name = fields.Char(string='Facility Name')
    room_ids = fields.Many2many('hotel.rooms', index=True)
