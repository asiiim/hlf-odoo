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