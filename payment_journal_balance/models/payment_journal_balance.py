# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class AccountPaymentsInherit(models.Model):
    _inherit = "account.payment"

    partner_balance  = fields.Monetary(compute='_credit_debit_get', search='inverse_credit_debit_get',
        string='Balance')
  
        


    @api.onchange('journal_id')
    def _credit_debit_get(self):
        for rec in self:
            domain = [('account_id','=',rec.journal_id.default_account_id.id)]
            move_lines = self.env['account.move.line'].search(domain)
            balance = 0
            for line in move_lines:
                balance += line.debit - line.credit
            rec.partner_balance = balance

                
    
    @api.onchange('partner_id')
    def inverse_credit_debit_get(self):
        for rec in self:
            domain = [('account_id','=',rec.journal_id.default_account_id.id)]
            move_lines = self.env['account.move.line'].search(domain)
            balance = 0
            for line in move_lines:
                balance += line.debit - line.credit
            rec.partner_balance = balance
