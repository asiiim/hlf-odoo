# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)


class HrEmployeeInherit(models.Model):
    _inherit = "hr.employee"

    corporate_title = fields.Char(string="Corporate Title")
    functional_title = fields.Char(string="Functional Title")
    level = fields.Char(string="Level")
    pan_number = fields.Char(string="PAN Number")
    ssf = fields.Char(string="SSF")
    pf = fields.Char(string="PF")
    cit_number = fields.Char(string="CIT Number")
    citizenship_no = fields.Char(string="Citizenship No.")
    issue_place = fields.Char(string="Issue Place")
    issue_date = fields.Date(string="Issue Date")
    blood_group = fields.Char(string="Blood Group")


class ContractInherit(models.Model):
    _inherit = "hr.contract"

    probation_date = fields.Date(string="Probation Date")
    probation_end_date = fields.Date(string="Probation End Date")
    first_supervisor = fields.Many2one('res.partner',string="First Supervisor")
    second_supervisor = fields.Many2one('res.partner',string="Second Supervisor")
    first_emergency_contact = fields.Many2one('res.partner',string="First Emergency Contact")
    second_emergency_contact = fields.Many2one('res.partner',string="Second Emergency Contact")


    


