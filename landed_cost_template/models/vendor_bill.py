# -*- coding: utf-8 -*-
# Part of Ten Orbits. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class VendorBill(models.Model):
    _inherit = 'account.move'

    @api.model
    def default_get(self, fields_list):
        default_vals = super(VendorBill, self).default_get(fields_list)
        if "landed_cost_template_id" in fields_list and not default_vals.get("landed_cost_template_id"):
            company_id = default_vals.get('company_id', False)
            company = self.env["res.company"].browse(company_id) if company_id else self.env.company
            default_vals['landed_cost_template_id'] = company.landed_cost_template_id.id
        return default_vals

    landed_cost_template_id = fields.Many2one(
        'sale.order.template', 'Landed Cost Template',
        readonly=True, check_company=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
