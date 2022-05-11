# -*- coding: utf-8 -*-
# Part of 10 Orbits Pvt. Ltd. See LICENSE for full copyright and licensing details.

from odoo import models, fields, api
import nepali_datetime


class ResConfigSettingsNepaliDate(models.TransientModel):
    _inherit = 'res.config.settings'

    DEFAULT_DATE_FORMAT = '%Y/%m/%d'
    bs_date_in_report = fields.Boolean(string='Date ? ', default=True)
    bs_datetime_in_report = fields.Boolean(string='DateTime ?', default=True)
    
    bs_date_format = fields.Char(string='Date Format', default=DEFAULT_DATE_FORMAT)
    bs_date_demo = fields.Char(string='Example')

    @api.onchange('bs_date_format')
    def _get_demo_nepali_date(self):
        if self.bs_date_format:
            dt =nepali_datetime.date(2078, 1, 26)
            self.bs_date_demo = dt.strftime(self.bs_date_format)


    #----------------------------------------------------------
    # Functions
    #----------------------------------------------------------
    
    # @api.multi
    def set_values(self):
        res = super(ResConfigSettingsNepaliDate, self).set_values()
        print("Printing Config Values")
        param = self.env['ir.config_parameter'].sudo()
        param.set_param('nepali_datepicker.bs_date_in_report', self.bs_date_in_report)
        param.set_param('nepali_datepicker.bs_datetime_in_report', self.bs_datetime_in_report)
        param.set_param('nepali_datepicker.bs_date_format', self.bs_date_format or '%Y/%m/%d')
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettingsNepaliDate, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            bs_date_in_report = bool(params.get_param('nepali_datepicker.bs_date_in_report')),
            bs_datetime_in_report =bool(params.get_param('nepali_datepicker.bs_datetime_in_report')),
            bs_date_format =params.get_param('nepali_datepicker.bs_date_format'),
        )
        return res






    
    

