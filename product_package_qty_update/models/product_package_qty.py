# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class SaleOrderLineInherit(models.Model):
    _inherit = "sale.order.line"

    
    @api.onchange('product_packaging')
    def product_packaging_qty_update(self):
        for rec in self:
            if rec.product_packaging:
                prodObj = self.env['product.product'].search([('id','=',rec.product_id.id)],limit=1)
                if prodObj:
                    for line in prodObj.packaging_ids:
                        if line.name == rec.product_packaging.name:
                            rec.product_uom_qty = line.qty
