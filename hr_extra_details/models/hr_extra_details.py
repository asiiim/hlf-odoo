# -*- coding: utf-8 -*-

import string
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)
from datetime import date,datetime
from dateutil.relativedelta import relativedelta


class HrCorporateTitle(models.Model):
    _name = "corporate.level.hr"
    _rec_name = 'level'

    level = fields.Integer(string="Corporate Level")
    corporate_title = fields.Char(string="Corporate Title")    


class HrFunctionalTitle(models.Model):
    _name = "functional.title.hr"
    
    name = fields.Char(string="Functional Title")


class HrContract(models.Model):
    _inherit = "hr.contract"

    probation_date = fields.Date( string="Probation Date")
    probation_duration = fields.Selection([
        ('one_month', '1 Month'),
        ('two_month', '2 Month'),
        ('three_month', '3 Month'),
        ('four_month', '4 Month'),
        ('five_month', '5 Month'),
        ('six_month', '6 Month'),
    ], string="Probation Duration")

    probation_end_date = fields.Date(string="Probation End Date",compute='_get_probation_end_date',store=True)

    @api.depends('probation_date','probation_duration')
    def _get_probation_end_date(self):
        for rec in self:
            if rec.probation_date and rec.probation_duration:
                if rec.probation_duration == 'one_month':
                    rec.probation_end_date = rec.probation_date + relativedelta(months=1)
                elif rec.probation_duration == 'two_month':
                    rec.probation_end_date = rec.probation_date + relativedelta(months=2)
                elif rec.probation_duration == 'three_month':
                    rec.probation_end_date = rec.probation_date + relativedelta(months=3)
                elif rec.probation_duration == 'four_month':
                    rec.probation_end_date = rec.probation_date + relativedelta(months=4)
                elif rec.probation_duration == 'five_month':
                    rec.probation_end_date = rec.probation_date + relativedelta(months=5)
                else:
                    rec.probation_end_date = rec.probation_date + relativedelta(months=6)

    first_emergency_contact = fields.Many2one('res.partner',string="First Emergency Contact")
    second_emergency_contact = fields.Many2one('res.partner',string="Second Emergency Contact")

    probation_end_date = fields.Date(string="Probation End Date",compute='_get_probation_end_date',store=True)

    @api.depends('probation_date','probation_duration')
    def _get_probation_end_date(self):
        for rec in self:
            if rec.probation_date and rec.probation_duration:
                if rec.probation_duration == 'one_month':
                    rec.probation_end_date = rec.probation_date + relativedelta(months=1)
                elif rec.probation_duration == 'two_month':
                    rec.probation_end_date = rec.probation_date + relativedelta(months=2)
                elif rec.probation_duration == 'three_month':
                    rec.probation_end_date = rec.probation_date + relativedelta(months=3)
                elif rec.probation_duration == 'four_month':
                    rec.probation_end_date = rec.probation_date + relativedelta(months=4)
                elif rec.probation_duration == 'five_month':
                    rec.probation_end_date = rec.probation_date + relativedelta(months=5)
                else:
                    rec.probation_end_date = rec.probation_date + relativedelta(months=6)

    first_emergency_contact = fields.Many2one('res.partner',string="First Emergency Contact")
    second_emergency_contact = fields.Many2one('res.partner',string="Second Emergency Contact")


class HrAppointmentType(models.Model):
    _name ="appointment.type.hr"

    name = fields.Char(string = "Appointment Type")



    
