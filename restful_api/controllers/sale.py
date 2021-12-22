from odoo import http
from odoo.http import request


class SaleController(http.Controller):
    
    @http.route('/api/v1/get_sale_orders/', type='json', auth='user')
    def get_sale_orders(self, **kw):
        sale_order_records = request.env['sale.order'].sudo().search([])
        sale_orders = []
        if sale_order_records:
            for rec in sale_order_records:
                vals = {
                'id': rec.id,
                'name': rec.name,
                'date_order': rec.date_order,
                'partner_id': rec.partner_id.id,
                'state': rec.state,
                'amount_total': rec.amount_total
            }
                sale_orders.append(vals)

        data = {
            'status': 200, 
            'response': sale_orders, 
            'message': 'Returned all sale order records'
        }
        return data

    
    @http.route('/api/v1/create_sale_order', type='json', auth='user')
    def create_sale_order(self, **rec):
        if request.jsonrequest:
            if rec['partner_id']:
                vals = {
                    'partner_id': rec['partner_id'],
                    'date_order': rec['date_order']
                }

                # Get current user from the session for sale responsible
                vals.update({'user_id': request.env.user.id})

                new_sale_order = request.env['sale.order']\
                .sudo().create(vals)
                args = {
                    'success': True, 
                    'message': 'Success', 
                    'id': new_sale_order.id,
                    'name': new_sale_order.name,
                    'status': 200
                }
        return args


    @http.route('/api/v1/create_sale_order_line', type='json', auth='user')
    def create_sale_order_line(self, **rec):
        if request.jsonrequest:
            if rec['order_id']:

                product_variant = request.env['product.product']\
                .search([('id', '=', rec['product_id'])])

                sale_order_env = request.env['sale.order']
                order_id = sale_order_env.search([('id', '=', rec['order_id'])])
                sale_orderline_env = request.env['sale.order.line']
                
                description = sale_orderline_env\
                .get_sale_order_line_multiline_description_sale(product_variant)

                vals = {
                    'order_id': rec['order_id'],
                    'partner_id': order_id.partner_id.id,
                    # 'name': rec['description'] or description,
                    'product_id': product_variant.id,
                    'product_uom_qty': rec['product_uom_qty']
                }

                # Get current user from the session for sale responsible
                vals.update({
                    'user_id': request.env.user.id,
                    'name': description
                })

                if not rec['price_unit']:
                    vals.update({'price_unit': product_variant.lst_price})
                else:
                    vals.update({'price_unit': rec['price_unit']})

                new_sale_order_line = sale_orderline_env.sudo().create(vals)
                args = {
                    'success': True, 
                    'message': 'Success', 
                    'id': new_sale_order_line.id,
                    'name': new_sale_order_line.name,
                    'status': 200
                }
        return args
