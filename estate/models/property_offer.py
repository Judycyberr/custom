from email.policy import default

from dateutil.relativedelta import relativedelta

from odoo import models, fields,api
from odoo.exceptions import UserError


class property_offer(models.Model):
    _name = 'property.offer'
    _description = 'Property Offer'
    price=fields.Float()
    status = fields.Selection(string="Status", selection=[('accepted','Accepted'),('refused','Refused')],copy=False)
    partner_id = fields.Many2one('res.partner', 'Buyer',required=True)
    property_id=fields.Many2one('estate.property','Property',required=True)
    validity=fields.Integer(default=7)
    date_deadline = fields.Date(compute='compute_deadline',inverse='inverse_deadline')
    create_date = fields.Date()

    @api.depends('validity')
    def compute_deadline(self):
        for record in self:
            if record.create_date :
                createdate = record.create_date.date()
            else:
                createdate = fields.Date.today()
            record.date_deadline = createdate + relativedelta(days=record.validity)


    def inverse_deadline(self):
        for record in self:
            if record.create_date :
                createdate = record.create_date.date()
            else:
                createdate = fields.Date.today()
            record.validity=record.date_deadline.day - createdate.day

    def action_confirm(self):
        for record in self:
                record.status = 'accepted'
                record.property_id.selling_price = record.price
                record.property_id.partner_id=record.partner_id

    def action_cancel(self):
        for record in self:
            record.status = 'refused'

