# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)


class ResBankBranch(models.Model):
    _name = "res.bank.branch"
    _description = "This is the branch of the bank from \
        where account has been opened."

    # Typically name for the branch which can be either address
    # or anything.
    name = fields.Char("Branch Name", required=True, copy=False)

    bank_id = fields.Many2one("res.bank", string="Bank", required=True)
    branch_code = fields.Char("Branch Code", copy=False)
    
    # Branch Address fields
    street = fields.Char()
    street2 = fields.Char()
    zip_code = fields.Char(change_default=True)
    city = fields.Char()

    state_id = fields.Many2one('res.country.state', 'State', 
        domain="[('country_id', '=?', country)]")
    country = fields.Many2one(related='bank_id.country')
    

    # Override create() method so that the branch name
    # will not get duplicated for different banks.
    @api.model
    def create(self, vals):
        
        # Assiging a name with bank short name to avoid branch
        # duplicate names
        name = vals['name']
        name += ' | '
        
        bank_name = self.env['res.bank'].search([
            ('id', '=', vals['bank_id'])]).name
        bank_short_name_list = [ b[0] for b in bank_name.split() ]
        bank_short_name = ""
        bank_short_name = bank_short_name.join(bank_short_name_list)
        
        name += bank_short_name
        vals['name'] = name
        
        result = super(ResBankBranch, self).create(vals)
        
        return result


    # Constraints
    _sql_constraints = [
        (
            'unique_name', 
            'UNIQUE(name)', 
            "Branch Already Exists !"
        ),
        (
            'unique_branch_code', 
            'UNIQUE(branch_code)', 
            "Branch Code Already Exists !"
        )
    ]
