# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class SaleOrderInherit(models.Model):
    _inherit = "sale.order"
    partner_balance  = fields.Monetary(compute='_credit_debit_get', search='inverse_credit_debit_get',
        string='Balance')
    

    @api.onchange('partner_id')
    def _credit_debit_get(self):
        for rec in self:
            if rec.partner_id.credit:
                rec.partner_balance = abs(rec.partner_id.credit)
            else:
                rec.partner_balance = 0

    
    @api.onchange('partner_id')
    def inverse_credit_debit_get(self):
        for rec in self:
            if rec.partner_id.credit:
                rec.partner_balance = abs(rec.partner_id.credit)
            else:
                rec.partner_balance = 0
    
class PurchaseOrderInherit(models.Model):
    _inherit = "purchase.order"
    partner_balance  = fields.Monetary(compute='_credit_debit_get', search='inverse_credit_debit_get',
        string='Balance')
    

    @api.onchange('partner_id')
    def _credit_debit_get(self):
        for rec in self:
            if rec.partner_id.debit:
                rec.partner_balance = abs(rec.partner_id.debit)
            else:
                rec.partner_balance = 0

    @api.onchange('partner_id')
    def inverse_credit_debit_get(self):
        for rec in self:
            if rec.partner_id.debit:
                rec.partner_balance = abs(rec.partner_id.debit)
            else:
                rec.partner_balance = 0

class AccountMoveInherit(models.Model):
    _inherit = "account.move"
    partner_balance  = fields.Monetary(compute='_credit_debit_get',search='inverse_credit_debit_get', 
        string='Balance')

    @api.onchange('partner_id')
    def _credit_debit_get(self):
        for rec in self:
            if rec.partner_id.debit:
                rec.partner_balance = abs(rec.partner_id.debit)
            elif rec.partner_id.credit:
                rec.partner_balance = abs(rec.partner_id.credit)
            else:
                rec.partner_balance = 0

            
    @api.onchange('partner_id')
    def inverse_credit_debit_get(self):
        for rec in self:
            if rec.partner_id.debit:
                rec.partner_balance = abs(rec.partner_id.debit)
            elif rec.partner_id.credit:
                rec.partner_balance = abs(rec.partner_id.credit)
            else:
                rec.partner_balance = 0

