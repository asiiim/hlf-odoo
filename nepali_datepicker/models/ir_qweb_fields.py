# -*- coding: utf-8 -*-
# Part of 10 Orbits Pvt. Ltd. See LICENSE for full copyright and licensing details.
import base64
import re
from collections import OrderedDict
from io import BytesIO
from odoo import api, fields, models, _
from PIL import Image
from lxml import etree, html
import nepali_datetime

import logging
_logger = logging.getLogger(__name__)



class NepaliDateConverter(models.AbstractModel):
    _inherit = 'ir.qweb.field.date'

    @api.model
    def value_to_html(self, value, options):
        res = super(NepaliDateConverter, self).value_to_html(value, options)
        if self.nepali_date_configuration():
            res = self.nepali_date_formatter(value, res)
        return res

    def nepali_date_configuration(self):
        params = self.env['ir.config_parameter'].sudo()
        bs_date_in_report = params.get_param('nepali_datepicker.bs_date_in_report')
        return bs_date_in_report

    def nepali_date_formatter(self, date_ad, date_string_ad):
        params = self.env['ir.config_parameter'].sudo()
        formatter = params.get_param('nepali_datepicker.bs_date_format')
        date_bs = nepali_datetime.date.from_datetime_date(date_ad).strftime(formatter)
        full_date = date_string_ad + " (" +str(date_bs)+")"
        return full_date

class NepaliDateTimeConverter(models.AbstractModel):
    _inherit = 'ir.qweb.field.datetime'

    @api.model
    def value_to_html(self, value, options):
        res = super(NepaliDateTimeConverter, self).value_to_html(value, options)
        
        if self.nepali_date_configuration():
            res = self.nepali_date_formatter(value, res)
        return res

    def nepali_date_configuration(self):
        params = self.env['ir.config_parameter'].sudo()
        bs_datetime_in_report = params.get_param('nepali_datepicker.bs_datetime_in_report')
        return bs_datetime_in_report

    def nepali_date_formatter(self, datetime_ad, datetime_string_ad):
        params = self.env['ir.config_parameter'].sudo()
        formatter = params.get_param('nepali_datepicker.bs_date_format')
        date_ad = datetime_ad.date()
        date_bs = nepali_datetime.date.from_datetime_date(date_ad).strftime(formatter)
        full_date = datetime_string_ad + " (" +str(date_bs)+")"
        return full_date


