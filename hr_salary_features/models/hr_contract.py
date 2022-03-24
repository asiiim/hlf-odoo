# -*- coding:utf-8 -*-

from odoo import api, fields, models


class HrContract(models.Model):
    
    _inherit = 'hr.contract'

    
    allowance = fields.Monetary(string="Allowance", help="Simply Allowance.")
    insurance = fields.Monetary(string="Insurance", help="Insurance.")
    cit = fields.Monetary(string="CIT", help="Citizen Investment Trust.")
