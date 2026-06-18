from email.policy import default

from dateutil.relativedelta import relativedelta

from odoo import models,fields,api
from odoo.exceptions import UserError, ValidationError
from odoo.orm.fields_numeric import Integer


class RealEstate(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Properties'
    name=fields.Char(required=True)
    description=fields.Text()
    property_type_id = fields.Many2one('property.type')
    postcode=fields.Char()
    date_availability=fields.Date(copy=False,default=fields.Date.today()+relativedelta(months=3))
    expected_price=fields.Float(required=True)
    selling_price=fields.Float(readonly=True,copy=False)
    bedrooms=fields.Integer(default=2)
    living_area=fields.Integer()

    facades=fields.Integer()
    garage=fields.Boolean()
    garage_area = fields.Integer()
    garden=fields.Boolean()
    garden_area=fields.Integer()


    total_area=fields.Integer(compute='compute_total')

    best_price=fields.Float(compute='compute_best_price')
    garden_orientation=fields.Selection(string='Garden Orientation',selection=[('north','North'),('south','South'),('east','East'),('west','West')])
    status=fields.Selection(string="Status",selection=[('new','New'),('offer recieved','Offer Recieved'),('offer accepted','Offer Accepted'),('sold','Sold'),('cancelled','Cancelled')],required=True,default='new',copy=False)
    active=fields.Boolean(default=True)
    user_id=fields.Many2one('res.users','SalesPerson',default=lambda self:self.env.user)
    partner_id=fields.Many2one('res.partner','Buyer')
    tag_ids=fields.Many2many('property.tag',string='Tags')
    offer_ids=fields.One2many('property.offer','property_id',string='Offers')


    @api.depends('living_area','garage_area')
    def compute_total(self):
        for record in self:
            record.total_area=record.living_area + record.garage_area

    @api.depends('offer_ids.price')
    def compute_best_price(self):
        for record in self:
            prices=record.offer_ids.mapped('price')
            if(len(prices)>0):
                record.best_price=max(prices)
            else:
                record.best_price=0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area=10
            self.garden_orientation='north'
        else:
            self.garden_area=0
            self.garden_orientation=False

    def sold(self):
        for record in self:
            if record.status == 'cancelled':
                raise UserError("Cancelled Properties can not be sold")
            else:
                record.status='sold'

    def cancel(self):
        for record in self:
            if record.status == 'sold':
                raise UserError("Sold Properties can not be cancelled")
            else:
                record.status='cancelled'

    @api.constrains('expected_price','selling_price','offer_ids.price')
    def _check_expected_price(self):
        for record in self:
            if record.expected_price<=0:
                raise ValidationError("price must be strictly positive")

    @api.constrains('selling_price','offer_ids.price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price<=0 or record.offer_ids.price<=0:
                raise ValidationError("price must be strictly positive")
            if record.selling_price<(90/100)*record.expected_price:
                raise ValidationError("price must be greater")


