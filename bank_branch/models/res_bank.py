# -*- coding: utf-8 -*-


from odoo import api, fields, models, _


class Bank(models.Model):
    _inherit = 'res.bank'

    branch_ids = fields.One2many('res.bank.branch', 'bank_id', string="Bank Branches")

