# -*- coding: utf-8 -*-
from flake8.formatting import default

from odoo import fields,models,api

from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError, UserError

from odoo.orm.fields_temporal import Date


class HotelAccommodation(models.Model):
    """All the fields and functions related to Hotel Accommodation"""
    _name = "hotel.accommodation"
    _description = "Accommodation"
    _rec_name = 'number'
    _inherit = 'mail.thread'

    number = fields.Char(required=True, readonly=True, default='New', copy=False)
    partner_id = fields.Many2one('res.partner', string="Customer", required=True, ondelete="cascade")
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    no_guest = fields.Integer(string="No. Guest", default=0, required=True)
    other_guest_id = fields.Many2one('res.partner', string="Other Members", ondelete="cascade")
    check_in = fields.Datetime(string="Check In", default=fields.Datetime.now, readonly=True)
    check_out = fields.Datetime(string="Check Out", readonly=True)
    room_id = fields.Many2one('hotel.rooms', string="Room", required=True, readonly = False, store=True, ondelete="cascade")
    room_ids = fields.Many2many('hotel.rooms', string="Rooms", compute='_get_rooms_domain', inverse='_inverse_rooms_domain')
    bed_type = fields.Selection(related="room_id.bed", readonly=False)
    facility_ids = fields.Many2many(related="room_id.facility_ids", string="Facility", readonly=False)
    state = fields.Selection([('draft', 'Draft'),('check_in', 'Check In'),('check_out', 'Check Out'),('cancel', 'Cancel')], "State", default='draft', tracking=True )
    description = fields.Text(string="Extra info")
    expected_days = fields.Integer(string="Expected Days", default=1)
    expected_date = fields.Date(string="Expected Date", compute="_compute_expected_date", inverse="_inverse_expected_date", default=lambda self: fields.Date.today() + relativedelta(days=1), store=True)
    guest_ids = fields.One2many('res.partner', 'accommodation_id', string="Guest", readonly=False, store=True, required=True)
    attachment_ids = fields.Many2many('ir.attachment')
    rent = fields.Float(related="room_id.rent", string="Rent", store=True)
    order_list_ids = fields.One2many('hotel.order.list', 'accommodation_id', string="Order List")
    item_total = fields.Float(string="Sub Total", related="order_list_ids.list_total")
    order_ids = fields.One2many('hotel.order.food', 'accommodation_id', string="Orders")
    service_product_ids = fields.One2many('hotel.payment.lines','accommodation_id', string="Service Product")
    # food_sub_total = fields.Float(related='order_ids.food_total_price')
    total = fields.Float(compute='_compute_total',string="Total: ")
    rent_sub_total = fields.Float(compute='_compute_rent_sub_total')
    invoice_id = fields.Many2one('account.move', string="Invoice")
    payment = fields.Selection(related = 'invoice_id.payment_state')
    cafe_count = fields.Integer()
    acc_room_type = fields.Selection(related='room_id.bed')
    acc_room_state = fields.Selection(related='room_id.state')
    cancel_date = fields.Date()
    active = fields.Boolean(default=True)


    @api.depends("bed_type","facility_ids")
    def _get_rooms_domain(self):
        """To set up domain for room"""
        if self.bed_type:
            rooms = self.env['hotel.rooms'].search([('bed', '=', self.bed_type)])
            self.room_ids = rooms
            if self.facility_ids:
                rooms = self.env['hotel.rooms'].search([('bed', '=', self.bed_type),('facility_ids', '=', self.facility_ids)])
                self.room_ids = rooms

        elif self.facility_ids:
            rooms = self.env['hotel.rooms'].search([('facility_ids', '=', self.facility_ids)])
            self.room_ids = rooms
            if self.bed_type:
                rooms = self.env['hotel.rooms'].search([('bed', '=', self.bed_type), ('facility_ids', '=', self.facility_ids)])
                self.room_ids = rooms
        else:
            self.room_ids = False

    def _inverse_rooms_domain(self):
        """Get the inverse domain from room"""
        if self.room_id:
            rooms=self.env['hotel.rooms'].search([('id', '=', self.room_id)])
            self.bed_type=rooms.bed_type
            self.facility_ids=rooms.facility_ids


    @api.model_create_multi
    def create(self, vals):
        """Create series of accommodation number"""
        for values in vals:
            if values.get('number' , 'New') == 'New':
                values['number'] = self.env['ir.sequence'].next_by_code('hotel.accommodation')
        return super(HotelAccommodation, self).create(vals)


    @api.depends('check_in', 'expected_days')
    def _compute_expected_date(self):
        """calculate the expected date"""
        for record in self:
            record.expected_date = record.check_in + relativedelta(days = record.expected_days)


    def _inverse_expected_date(self):
        """calculate the expected days"""
        for record in self:
            record.expected_days = (record.expected_date - record.check_in.date()).days


    def action_check_in(self):
        """things to perform when clicking the check-in button"""
        for record in self:
            record.attachment_ids = record.env['ir.attachment'].search([('res_model', '=', record._name),('res_id', '=', record.id)])
            if not record.attachment_ids.ids:
                raise ValidationError("No Attachment Found")
            record.state = 'check_in'
            record.check_in = fields.Datetime.now()
            record._compute_expected_date()
            record.room_id.state = 'not_available'

            product_2 = self.env.ref('hotel_management.product_2')
            self.env['hotel.payment.lines'].create({
                'product_id': product_2.id,
                'accommodation_id': self.id,
                'price': self.rent
            })




    def action_check_out(self):
        """things to perform when clicking the check-out button"""
        for record in self:
            record.state = 'check_out'
            record.check_out = fields.Datetime.now()
            record.room_id.state = 'available'
            lines = []
            for rec in record.service_product_ids:
                lines.append([0,0,{
                    'product_id': rec.product_id.id,
                    'price_unit': rec.price
                }])
            self.invoice_id = record.env['account.move'].create({
                'move_type':'out_invoice',
                'invoice_date': fields.Datetime.now(),
                'partner_id': self.partner_id.id,
                'invoice_line_ids': lines
            })
        return {
            'name': 'Draft Invoices',
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'current',
            'res_id': self.invoice_id.id,
        }


    def action_cancel(self):
        """things to perform when clicking the cancel button"""
        for record in self:
            record.state = 'cancel'
            record.room_id.state = 'available'
            record.cancel_date = fields.Date.today()


    @api.constrains('guest_ids','no_guest')
    def _check_no_guest(self):
        """check the number of guests is equal to the number of guests entered"""
        for record in self:
            if len(record.guest_ids) != record.no_guest:
                raise ValidationError("Number of guests not equal to total guest entered")

    @api.depends('rent_sub_total','item_total')
    def _compute_total(self):
        """To calculate the total of rent and restaurant expenses"""
        product_2 = self.env.ref('hotel_management.product_2')
        for record in self:
            record.total = record.rent_sub_total + record.item_total
            product_2.update({'lst_price': record.rent_sub_total})

        count = 0
        for record in self.env['hotel.order.food'].search([('accommodation_id', 'in', self.ids)]):
            count += 1
        self.cafe_count = count

    @api.depends('rent','check_out')
    def _compute_rent_sub_total(self):
        """To calculate the sub-total of rent"""
        product_2 = self.env.ref('hotel_management.product_2')
        self.rent_sub_total = self.rent
        if self.check_out and not self.invoice_id:
            for record in self:
                record.rent_sub_total = record.rent * (record.check_out.date() - record.check_in.date()).days
                product_2.update({'lst_price': record.rent_sub_total})


    def action_view_invoice(self):
        """To display the form view of invoice details on the same screen"""
        return {
            'name': 'Draft Invoices',
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'current',
            'res_id': self.invoice_id.id,
        }

    def action_view_invoice_cafe(self):
        """To display the list view of  invoices on the same screen"""
        return {
            'name': 'Food Details',
            'type': 'ir.actions.act_window',
            'res_model': 'hotel.order.food',
            'view_mode': 'list',
            'view_type': 'list',
            'target': 'current',
            'domain': [('accommodation_id', 'in', self.ids)],
        }

    def send_mail(self):
        """Send mail to customer"""
        template = self.env['mail.template'].browse(self.env.ref('hotel_management.mail_template_check_out').id)
        acc = self.search([
            ('expected_date', '=', Date.today()),
            ('state', '=', 'check_in'),
            ])
        if template:
            if acc:
                for record in acc:
                    template.send_mail(record.id, force_send=True)
        else:
            raise UserError("Mail Template not found. Please check the template.")

    @api.model
    def check_archive(self):
        """To archive the records after 2 days from cancellation date"""
        acc_ids = self.env['hotel.accommodation'].search([('state', '=', 'cancel')])
        for rec in acc_ids:
            if rec.cancel_date:
                cancel_date = rec.cancel_date
                curr_date = Date.today()
                days = (curr_date - cancel_date).days
                if days >= 2:
                    rec.active = False



