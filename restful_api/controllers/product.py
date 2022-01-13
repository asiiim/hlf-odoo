from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale



class ProductCategoryController(http.Controller):
    
    @http.route('/api/v1/get_product_categories/', type='json', auth='user')
    def get_product_categories(self, **kw):
        product_category_records = request.env['product.category'].sudo().search([])
        product_categories = []
        if product_category_records:
            for rec in product_category_records:
                vals = {
                'id': rec.id,
                'name': rec.name
            }
                product_categories.append(vals)

        data = {
            'status': 200, 
            'response': product_categories, 
            'message': 'Returned all product category records'
        }
        return data

    
    @http.route('/api/v1/create_product_category', type='json', auth='user')
    def create_product_category(self, **rec):
        if request.jsonrequest:
            if rec['name']:
                vals = {
                    'name': rec['name'],
                }
                new_product_category = request.env['product.category']\
                .sudo().create(vals)
                args = {
                    'success': True, 
                    'message': 'Success', 
                    'id': new_product_category.id,
                    'status': 200
                }
        return args


    @http.route('/api/v1/update_product_category', type='json', auth='user')
    def update_product_category(self, **rec):
        if request.jsonrequest:
            if rec['id']:
                product_category = request.env['product.category']\
                .sudo().search([('id', '=', rec['id'])])
                if product_category:
                    product_category.sudo().write(rec)
                args = {
                    'success': True, 
                    'message': 'Product Category Updated',
                    'status': 200
                }
        return args



class ProductTemplateController(http.Controller):
    
    @http.route('/api/v1/get_product_templates/', type='json', auth='user')
    def get_product_templates(self, **kw):
        product_template_records = request.env['product.template'].sudo().search([])
        product_templates = []

        if product_template_records:
            for rec in product_template_records:
                vals = {
                'id': rec.id,
                'name': rec.name,
                'type': rec.type,
                'categ_id': rec.categ_id.id,
                'uom_id': rec.uom_id.id
            }
                product_templates.append(vals)

        data = {
            'status': 200, 
            'response': product_templates, 
            'message': 'Returned all product template records'
        }
        return data


    @http.route('/api/v1/get_product_variants/', type='json', auth='user')
    def get_product_variants(self, **kw):
        product_variant_records = request.env['product.product'].sudo().search([])
        product_variants = []

        if product_variant_records:
            for rec in product_variant_records:
                vals = {
                'id': rec.id,
                'name': rec.name,
                'type': rec.type,
                'categ_id': rec.categ_id.id,
                'uom_id': rec.uom_id.id
            }
                product_variants.append(vals)

        data = {
            'status': 200, 
            'response': product_variants, 
            'message': 'Returned all product variant records'
        }
        return data


    @http.route('/api/v1/get_uom_list/', type='json', auth='user')
    def get_uom_list(self, **kw):
        uom_records = request.env['uom.uom'].sudo().search([])
        uoms = []

        if uom_records:
            for rec in uom_records:
                vals = {
                'id': rec.id,
                'name': rec.name,
                'uom_type': rec.uom_type,
                'category_id': rec.category_id.id,
            }
                uoms.append(vals)

        data = {
            'status': 200, 
            'response': uoms, 
            'message': 'Returned all unit of measurement records'
        }
        return data

    
    @http.route('/api/v1/create_product_template', type='json', auth='user')
    def create_product_template(self, **rec):
        if request.jsonrequest:
            if rec['name']:
                vals = {
                    'name': rec['name'],
                    'categ_id': rec['categ_id'],
                    'type': rec['type'],
                    'default_code': rec['default_code'],
                    'uom_id': rec['uom_id'],
                    'uom_po_id': rec['uom_po_id'],
                    'list_price': rec['list_price'],
                    'standard_price': rec['standard_price']
                }
                new_product_template = request.env['product.template']\
                .sudo().create(vals)
                args = {
                    'success': True, 
                    'message': 'Success', 
                    'id': new_product_template.id,
                    'status': 200
                }
        return args


    @http.route('/api/v1/update_product_template', type='json', auth='user')
    def update_product_template(self, **rec):
        if request.jsonrequest:
            if rec['id']:
                product_template = request.env['product.template']\
                .sudo().search([('id', '=', rec['id'])])
                if product_template:
                    product_template.sudo().write(rec)
                args = {
                    'success': True, 
                    'message': 'Product Template Updated',
                    'status': 200
                }
        return args



class ProductAttributeController(http.Controller):
    
    @http.route('/api/v1/get_product_attributes/', type='json', auth='user')
    def get_product_attributes(self, **kw):
        product_attribute_records = request.env['product.attribute'].sudo().search([])
        product_attributes = []

        if product_attribute_records:
            for rec in product_attribute_records:
                vals = {
                'id': rec.id,
                'name': rec.name,
                'sequence': rec.sequence,
                'type': rec.type,
                'display_name': rec.display_name
            }
                product_attributes.append(vals)

        data = {
            'status': 200, 
            'response': product_attributes, 
            'message': 'Returned all product attribute records'
        }
        return data


    def get_product_attribute_values(self, **kw):
        product_attribute_value_records = request.env['product.attribute.value']\
        .sudo().search([])
        product_attribute_values = []

        if product_attribute_value_records:
            for rec in product_attribute_value_records:
                vals = {
                'id': rec.id,
                'name': rec.name,
                'sequence': rec.sequence,
                'html_color': rec.html_color,
                'is_custom': rec.is_custom,
                'attribute_id': rec.attribute_id.id
            }
                product_attribute_values.append(vals)

        data = {
            'status': 200, 
            'response': product_attribute_values, 
            'message': 'Returned all product attribute value records'
        }
        return data

    
    @http.route('/api/v1/create_product_attribute', type='json', auth='user')
    def create_product_attribute(self, **rec):
        if request.jsonrequest:
            if rec['name']:
                vals = {
                    'name': rec['name'],
                    'sequence': rec['sequence'],
                    'type': rec['type']
                }
                new_product_attribute = request.env['product.attribute']\
                .sudo().create(vals)
                args = {
                    'success': True, 
                    'message': 'Success', 
                    'id': new_product_attribute.id,
                    'status': 200
                }
        return args


    @http.route('/api/v1/create_product_attribute_value', type='json', auth='user')
    def create_product_attribute_value(self, **rec):
        if request.jsonrequest:
            if rec['name']:
                vals = {
                    'name': rec['name'],
                    'sequence': rec['sequence'],
                    'html_color': rec['html_color'],
                    'is_custom': rec['is_custom'],
                    'attribute_id': rec['attribute_id']
                }
                new_product_attribute_value = request.env['product.attribute.value']\
                .sudo().create(vals)
                args = {
                    'success': True, 
                    'message': 'Success', 
                    'id': new_product_attribute_value.id,
                    'status': 200
                }
        return args
