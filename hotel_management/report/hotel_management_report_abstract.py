# -*- coding: utf-8 -*-
from odoo import models,api

class HotelManagementReportAbstract(models.AbstractModel):
    """Abstract model for hotel management report"""
    _name = 'report.hotel_management.report_hotel_management'

    @api.model
    def _get_report_values(self, docids, data=None):
        """get the report values"""
        # for record in self.env['hotel.accommodation'].search([]):
        #     docids.append(record.id)
        # print('Docids:', docids)
        # print('data:', data)
        # docs = self.env['hotel.accommodation'].browse(docids)
        # print('Data',data)
        # print('Docs',docs)
        return {
            # 'doc_ids': docids,
            'doc_model': 'hotel.accommodation',
            'data': data,
            # 'docs': docs,
        }