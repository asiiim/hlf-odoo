# -*- coding: utf-8 -*-
# Part of Ten Orbits. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class LandedCostTemplate(models.Model):
    _name = "landed.cost.template"
    _description = "Landed Cost Template"


    name = fields.Char('Landed Cost Template', required=True)
    landed_cost_template_line_ids = fields.One2many('landed.cost.template.line', 'landed_cost_template_id', 'Lines', copy=True)
    note = fields.Text('Terms and conditions', translate=True)
    active = fields.Boolean(default=True, help="If unchecked, it will allow you to hide the template without removing it.")
    company_id = fields.Many2one(
        'res.company', 
        'Company', required=True, index=True, 
        default=lambda self: self.env.user.company_id.id)

    @api.constrains('company_id', 'landed_cost_template_line_ids')
    def _check_company_id(self):
        for template in self:
            companies = template.mapped('landed_cost_template_line_ids.product_id.company_id')
            if len(companies) > 1:
                raise ValidationError(_("Your template cannot contain products from multiple companies."))
            elif companies and companies != template.company_id:
                raise ValidationError(_(
                    "Your template contains products from company %(product_company)s whereas your template belongs to company %(template_company)s. \n Please change the company of your template or remove the products from other companies.",
                    product_company=', '.join(companies.mapped('display_name')),
                    template_company=template.company_id.display_name,
                ))

    @api.onchange('landed_cost_template_line_ids')
    def _onchange_template_line_ids(self):
        companies = self.mapped('landed_cost_template_line_ids.product_id.company_id')
        if companies and self.company_id not in companies:
            self.company_id = companies[0]

    
    journal_id = fields.Many2one('account.journal', 
        string='Journal',
        check_company=True, domain="[('id', 'in', suitable_journal_ids)]",
        required=True)
    suitable_journal_ids = fields.Many2many('account.journal', compute='_compute_suitable_journal_ids')

    @api.depends('company_id')
    def _compute_suitable_journal_ids(self):
        for m in self:
            journal_type = 'purchase'
            company_id = m.company_id.id or self.env.company.id
            domain = [('company_id', '=', company_id), ('type', '=', journal_type)]
            m.suitable_journal_ids = self.env['account.journal'].search(domain)



class LandedCostTemplateLine(models.Model):
    _name = "landed.cost.template.line"
    _description = "Landed Cost Template Line"
    _order = 'landed_cost_template_id, sequence, id'

    sequence = fields.Integer('Sequence', help="Gives the sequence order when displaying a list of landed cost lines.",
        default=10)
    landed_cost_template_id = fields.Many2one(
        'landed.cost.template', 'Landed Cost Template Reference',
        required=True, ondelete='cascade', index=True)
    company_id = fields.Many2one('res.company', related='landed_cost_template_id.company_id', store=True, index=True)
    account_id = fields.Many2one('account.account', string='Account',
        index=True, ondelete="cascade",
        domain="[('deprecated', '=', False), ('company_id', '=', company_id),('is_off_balance', '=', False)]",
        check_company=True,
        tracking=True)
    is_landed_costs_line = fields.Boolean('Is Landed Cost', default=True, readonly=True)
    name = fields.Text('Description', required=True, translate=True)
    product_id = fields.Many2one(
        'product.product', 'Product', check_company=True)
    product_uom_qty = fields.Float('Quantity', required=True, digits='Product Unit of Measure', default=1)
    product_uom_id = fields.Many2one('uom.uom', 'Unit of Measure', domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id', readonly=True)


    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.ensure_one()
        if self.product_id:
            self.product_uom_id = self.product_id.uom_id.id
            self.name = self.product_id.name


    _sql_constraints = [
        ('accountable_product_id_required',
            "CHECK(product_id IS NOT NULL AND product_uom_id IS NOT NULL)",
            "Missing required product and UoM on accountable sale quote line."),
    ]
