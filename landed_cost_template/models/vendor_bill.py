# -*- coding: utf-8 -*-
# Part of Ten Orbits. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class VendorBill(models.Model):
    _inherit = 'account.move'


    landed_cost_template_id = fields.Many2one(
        'landed.cost.template', 'Landed Cost Template',
        readonly=True, check_company=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")

    
    
    def _compute_line_data_for_template_change(self, line):
        return {
            'name': line.name,
        }

    
    @api.onchange('landed_cost_template_id')
    def onchange_landed_cost_template_id(self):

        template = self.landed_cost_template_id.with_context(lang=self.partner_id.lang)

        order_lines = [(5, 0, 0)]
        for line in template.landed_cost_template_line_ids:

            data = self._compute_line_data_for_template_change(line)

            if line.product_id:
                price = line.product_id.standard_price
                discount = 0


                data.update({
                    'price_unit': price,
                    'discount': discount,
                    'quantity': line.product_uom_qty,
                    'product_id': line.product_id.id,
                    'product_uom_id': line.product_uom_id.id,
                    'is_landed_costs_line': line.is_landed_costs_line,
                    'account_id': line.account_id.id,
                    'currency_id': line.company_id.currency_id.id,
                    'partner_id': self.partner_id,

                })

            order_lines.append((0, 0, data))

        self.invoice_line_ids = order_lines
        
        # Compute subtotal of each line
        for line in self.invoice_line_ids:
            line._onchange_account_id()
