# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)
from datetime import date,datetime
from dateutil.relativedelta import relativedelta

class HrEmployeeInherit(models.Model):
    _inherit = "hr.employee"

    corporate_level = fields.Many2one('corporate.level.hr',string="Corporate Level")
    corporate_title = fields.Char(related='corporate_level.corporate_title',store=True)
    functional_title = fields.Many2one('functional.title.hr',string="Functional Title")
    level = fields.Char(string="Level")
    pan_number = fields.Char(string="PAN Number")
    ssf = fields.Char(string="SSF")
    pf = fields.Char(string="PF")
    cit_number = fields.Char(string="CIT Number")
    citizenship_no = fields.Char(string="Citizenship No.")
    issue_place = fields.Char(string="Issue Place")
    issue_date = fields.Date(string="Issue Date")
    blood_group = fields.Selection([
        ('A+', 'A RhD positive'),
        ('A-)', 'A RhD negative'),
        ('B+', 'B RhD positive'),
        ('B-', 'B RhD negative'),
        ('O+', 'O RhD positive'),
        ('O-', 'O RhD negative'),
        ('AB+', 'AB RhD positive'),
        ('AB-', 'AB RhD negative'),
    ], string="Blood Group")

    first_supervisor = fields.Many2one('res.users',string="First Supervisor")
    second_supervisor = fields.Many2one('res.users',string="Second Supervisor")
  
class CorporateTitle(models.Model):
    _name = "corporate.level.hr"
    _rec_name = 'level'

    level = fields.Integer(string="Corporate Level")
    corporate_title = fields.Char(string="Corporate Title")    


class FunctionalTitle(models.Model):
    _name = "functional.title.hr"

    
    name = fields.Char(string="Functional Title")




class ContractInherit(models.Model):
    _inherit = "hr.contract"

    probation_date = fields.Date(string="Probation Date")
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
