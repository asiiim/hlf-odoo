# -*- coding: utf-8 -*-

from ast import literal_eval

from odoo import api, fields, models, _

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)







