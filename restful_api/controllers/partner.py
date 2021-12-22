from odoo import http
from odoo.http import request



class ResPartnerController(http.Controller):

    @http.route('/api/v1/get_customers', type='json', auth='user')
    def get_customers(self, **kw):
        customer_records = request.env['res.partner'].sudo().search([])
        customers = []
        if customer_records:
            for rec in customer_records:
                vals = {
                    'id': rec.id,
                    'name': rec.name
                }
                customers.append(vals)

        data = {
            'status': 200, 
            'response': customers, 
            'message': 'Returned all customer records'
        }
        return data

    
    @http.route('/api/v1/create_customer', type='json', auth='user')
    def create_customer(self, **rec):
        if request.jsonrequest:
            if rec['name']:
                vals = {
                    'name': rec['name'],
                    'email': rec['email'],
                    'street': rec['street'],
                    'street2': rec['nearby'],
                    'city': rec['city'],
                    'vat': rec['tax_id']
                }
                new_customer = request.env['res.partner'].sudo().create(vals)
                args = {
                    'success': True, 
                    'message': 'Success', 
                    'id': new_customer.id,
                    'status': 200
                }
        return args


    @http.route('/api/v1/update_customer', type='json', auth='user')
    def update_customer(self, **rec):
        if request.jsonrequest:
            if rec['id']:
                customer = request.env['res.partner'].sudo()\
                .search([('id', '=', rec['id'])])
                if customer:
                    
                    # Here tax_id and nearby keys are assigned to regular keys
                    if rec["tax_id"] or rec["nearby"]:
                        rec.update({
                            'vat': rec["tax_id"] or "",
                            'street2': rec["nearby"] or ""
                        })
                    
                    customer.sudo().write(rec)
                
                args = {
                    'success': True, 
                    'message': 'Customer Updated',
                    'status': 200,
                    'id': customer.id
                }
        return args
