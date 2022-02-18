# -*- coding: utf-8 -*-
# Part of Ten Orbits Pvt. Ltd. See LICENSE file for full copyright and licensing details.

from odoo.osv import expression
from odoo import api, fields, models, _


class ResDistrict(models.Model):
    _description = "Country district"
    _name = 'res.district'
    _order = 'name'

    state_id = fields.Many2one('res.country.state', string='State', required=True)
    country_id = fields.Many2one('res.country', related='state_id.country_id', string='Country', readonly=True)
    name = fields.Char(string='District Name', required=True,
               help='Administrative districts of a state. E.g. Kaski district, Gandaki state, Nepal')
    code = fields.Char(string='District Code', help='The district code.')

    _sql_constraints = [
        ('name_code_uniq', 'unique(state_id, code)', 'The code of the district must be unique by state !')
    ]

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if self.env.context.get('state_id'):
            args = expression.AND([args, [('state_id', '=', self.env.context.get('state_id'))]])

        if operator == 'ilike' and not (name or '').strip():
            first_domain = []
            domain = []
        else:
            first_domain = [('code', '=ilike', name)]
            domain = [('name', operator, name)]

        first_district_ids = self._search(expression.AND([first_domain, args]), limit=limit, access_rights_uid=name_get_uid) if first_domain else []
        return list(first_district_ids) + [
            district_id
            for district_id in self._search(expression.AND([domain, args]),
                                         limit=limit, access_rights_uid=name_get_uid)
            if district_id not in first_district_ids
        ]

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "{} ({})".format(record.name, record.state_id.code)))
        return result