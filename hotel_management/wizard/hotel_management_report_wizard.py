# -*- coding: utf-8 -*-
import datetime
import io

import xlsxwriter, json
from dateutil.rrule import rrule, DAILY
from datetime import datetime

from odoo import fields, models, api
from odoo.tools import json_default


class HotelManagementReportWizard(models.TransientModel):
    """Wizard for taking requirement for report"""
    _name = 'hotel.management.report.wizard'

    date_from = fields.Date(string='Date from')
    date_to = fields.Date(string='Date to')
    partner_id = fields.Many2one('res.partner', string='Customer Name')
    accommodation_id = fields.Many2one('hotel.accommodation', string='Accommodation id')
    state = fields.Selection(related='accommodation_id.state', string='State', readonly=False, store=True)

    def create_report(self):
        """All the query and the report creation"""

        query = """select pr.name, ac.number, ac.check_in, ac.check_out, ac.state from hotel_accommodation as ac
                inner join res_partner as pr on pr.id = ac.partner_id"""

        if self.date_from or self.date_to or self.partner_id or self.state:
            if self.date_from:
                query += f""" where ac.check_in >= '{self.date_from}'"""
                print("before function", query)
                query += self.add_query()
                print("after function", query)

            elif self.date_to:
                query += f""" where ac.check_out <= '{self.date_to}'"""
                query += self.add_query()

            elif self.partner_id:
                query += f""" where pr.id = '{self.partner_id.id}'"""
                query += self.add_query()

            elif self.state:
                query += f""" where ac.state = '{self.state}'"""
                query += self.add_query()

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        data = {'report': report}
        print(data)
        return self.env.ref('hotel_management.action_report_hotel_management').report_action(None, data = data)

    def add_query(self):
        query = ""
        if self.date_from:
            query += f""" and ac.check_in >= '{self.date_from}'"""
        if self.date_to:
            query += f""" and ac.check_out <= '{self.date_to}'"""
        if self.partner_id:
            query += f""" and pr.id = '{self.partner_id.id}'"""
        if self.state:
            query += f""" and ac.state = '{self.state}'"""

        return query

    def add_query_xlsx(self, data):
        query = ""
        if data.get('date_from'):
            query += f""" and ac.check_in >= '{data.get('date_from')}'"""
        if data.get('date_to'):
            query += f""" and ac.check_out <= '{data.get('date_to')}'"""
        if data.get('partner_id'):
            query += f""" and pr.id = '{data.get('partner_id')}'"""
        if data.get('state'):
            query += f""" and ac.state = '{data.get('state')}'"""

        return query

    def action_print_xlsx(self):
        """
        Returns report action for the XLSX Attendance report
        Raises: ValidationError: if From Date > To Date
        Raises: ValidationError: if there is no attendance records
        Returns:
            dict:  the XLSX report action
        """
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'partner_id': self.partner_id.id,
            'state':self.state
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'hotel.management.report.wizard',
                     'options': json.dumps(data, default=json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Accommodation Report',
                     },
            'report_type': 'xlsx',
        }

    @api.model
    def get_xlsx_report(self, data, response):
        """
        Print the XLSX report
        Returns: None
        """
        print("got the xl report")
        query = """select pr.name, ac.number, ac.check_in, ac.check_out, ac.state from hotel_accommodation as ac
                        inner join res_partner as pr on pr.id = ac.partner_id"""

        if data.get('date_from') or data.get('date_to') or data.get('partner_id') or data.get('state'):
            if data.get('date_from'):
                query += f""" where ac.check_in >= '{data.get('date_from')}'"""
                query += self.add_query_xlsx(data)

            elif data.get('date_to'):
                query += f""" where ac.check_out <= '{data.get('date_to')}'"""
                query += self.add_query_xlsx(data)

            elif data.get('partner_id'):
                query += f""" where pr.id = '{data.get('partner_id')}'"""
                query += self.add_query_xlsx(data)

            elif data.get('state'):
                query += f""" where ac.state = '{data.get('state')}'"""
                query += self.add_query_xlsx(data)

        self.env.cr.execute(query)
        docs = self.env.cr.dictfetchall()
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('docs')
        sheet.set_column('D:H', 20)
        border = workbook.add_format({'border': 1})
        head = workbook.add_format(
            {'bold': True, 'font_size': 30, 'align': 'center'})
        date_size = workbook.add_format(
            {'font_size': 12, 'bold': True, 'align': 'center', 'text_wrap': True})
        sheet.merge_range('C3:K6', 'Accommodation Report', head)
        if data.get('date_from'):
            sheet.merge_range('B8:D9', 'From Date: ' + data['date_from'], date_size)
        if data.get('date_to'):
            sheet.merge_range('B10:D11', 'To Date: ' + data['date_to'], date_size)
        if data['partner_id']:
            sheet.merge_range('B12:D13', 'Customer: ' + self.env['res.partner'].browse(data['partner_id']).name, date_size)
        sheet.merge_range('D16:D17', 'Sl.No', border)
        sheet.merge_range('E16:E17', 'Customer', border)
        sheet.merge_range('F16:F17', 'Check-in', border)
        sheet.merge_range('G16:G17', 'Check-out', border)
        sheet.merge_range('H16:H17', 'State', border)
        date_style = workbook.add_format({'text_wrap': True, 'num_format': 'dd-mm-yyyy'})
        row = 16
        for rec in docs:
            col =2
            row += 1
            col += 1
            print(rec)
            sheet.write(row, col, rec['number'])
            col += 1
            sheet.write(row, col, rec['name'])
            col += 1
            sheet.write(row, col, rec['check_in'], date_style)
            col += 1
            sheet.write(row, col, rec['check_out'], date_style)
            col += 1
            sheet.write(row, col, rec['state'])
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()