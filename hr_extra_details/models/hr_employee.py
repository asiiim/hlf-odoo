# -*- coding: utf-8 -*-
# Part of Ten Orbits Pvt. Ltd. See LICENSE file for full copyright and licensing details.

from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _


class HrEmployeePrivate(models.Model):
    _inherit = 'hr.employee'
    
    joining_date = fields.Datetime(
        'Joining Date', 
        default=fields.Datetime.now, 
        tracking=True,
        help="Joining date of the employee.")

    last_login_date = fields.Datetime(
        related='user_id.login_date', string='Last Login', readonly=False,
        store=True)

    
    # Add district data
    district_id = fields.Many2one('res.district', string='District')
    district_name = fields.Char(related='district_id.name', string='District Name')


    corporate_level = fields.Many2one('corporate.level.hr',string="Corporate Level")
    corporate_title = fields.Char(related='corporate_level.corporate_title',store=True)
    functional_title = fields.Many2one('functional.title.hr',string="Functional Title")
    appointment_type =fields.Many2one('appointment.type.hr',string ="Appointment Type")
    level = fields.Char(string="Level")
    pan_number = fields.Char(string="PAN Number")
    ssf = fields.Char(string="SSF")
    pf = fields.Char(string="PF")
    cit_number = fields.Char(string="CIT Number")
    citizenship_no = fields.Char(string="Citizenship No.")
    issue_place = fields.Char(string="Issue Place")
    issue_date = fields.Date(string="Issue Date")
    promotion_date = fields.Date(string ="Promotion Date")
    transfer_date = fields.Date(string ="Transfer Date")
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
    

    first_supervisor = fields.Many2one('hr.employee',string="First Supervisor")
    second_supervisor = fields.Many2one('hr.employee',string="Second Supervisor")
    transfer_department = fields.Many2one('hr.department',string="Transfer Department")
