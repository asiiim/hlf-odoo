# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2019-today Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################

from odoo import api, fields, models, _
from dateutil.parser import parse
from odoo.exceptions import UserError
import datetime
import pytz
import logging
_logger = logging.getLogger(__name__)


class InvoiceOutstanding(models.TransientModel):
    _name = "invoice.outstanding.wiz"

    start_date = fields.Date(string='From Date', required='1', help='select start date')
    end_date = fields.Date(string='To Date', required='1', help='select end date')
    total_amount_due = fields.Integer(string='Total Outstanding Amount')

    def _get_report_base_filename(self):
        self.ensure_one()
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        return  _('Invoice Report - %s') % (docs.start_date)

    '''Find Outstanding invoices between the date and find total outstanding amount'''
    @api.model
    def _get_report_values(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        outstanding_invoice = []       
       
        invoices = self.env['account.move'].search([('date_invoice', '>=', docs.start_date),('date_invoice', '<=', docs.end_date),('move_type','=', 'out_invoice'),('state','in',['in_payment','open','paid'])])
        if invoices:
            amount_due = 0
            for total_amount in invoices:
                amount_due += total_amount.amount_total
            docs.total_amount_due = amount_due

            return {
                'docs': docs,
                'invoices': invoices,
            }
        else:
            raise UserError("No record found!")

    def check_report(self):
        data = {}
        data['form'] = self.read(['start_date', 'end_date'])[0]
        return self._print_report(data)
    

    #     # data['form'] = self.read(['start_date', 'end_date'])[0]
    #     # return self._print_report_xlsx(data)

    def _print_report(self, data):
        data['form'].update(self.read(['start_date', 'end_date'])[0])
        return self.env.ref('invoice_outstanding_report.action_customer_invoice_outstanding').report_action(self, data=data, config=False)
    def check_report_xlsx(self):
        context = self._context
        
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'invoice.outstanding.wiz'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        # if context.get('xls_export'):
        return self.env.ref('invoice_outstanding_report.action_customer_invoice_outstanding_xlsx').report_action(self, data=datas)


    

   