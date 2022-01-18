# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    bank_branch = fields.Many2one('res.bank.branch', string="Branch", \
        domain="[('bank_id', '=', bank_id)]", default=None, required=True)

    @api.onchange('bank_id')
    def onchange_bank(self):
        """ This method clears the branch field when changing the bank \
            in the bank account form view. 
        """
        self.bank_branch = None
