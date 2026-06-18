# -*- coding: utf-8 -*-
from odoo import fields,models


class HotelRooms(models.Model):
    """All the fields related to Hotel Rooms"""
    _name = 'hotel.rooms'
    _description = 'Rooms'
    _rec_name = 'room_no'
    
    room_no = fields.Integer(string='Room Number', required=True)
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    bed = fields.Selection(string='bed', selection=[('single', 'Single'), ('double', 'Double'), ('dormitory', 'Dormitory')])
    available_beds = fields.Integer()
    rent = fields.Float(string='Rent')
    state = fields.Selection(string='State', selection=[('available', 'Available'),('not_available', 'Not Available')])
    facility_ids = fields.Many2many('hotel.facility', index=True)
