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

import time
from odoo import api, models, _
from dateutil.parser import parse
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from datetime import datetime
import pytz
import logging
_logger = logging.getLogger(__name__)




    # def _get_xlsx_report_base_filename(self):
    #     self.ensure_one()
    #     _logger.info('==========================tet====',)

    #     docs = self.env[self.model].browse(self.env.context.get('active_id'))
    #     _logger.info('==========================d====%s',docs)
    #     return  _('Invoice Report - %s') % (docs.start_date)
        
    


class ReportXlsxOutstanding(models.AbstractModel):
    _name = 'report.invoice_outstanding_report.invoice_outstanding_wiz'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):

        _logger.info('=================lines======%s',lines)
        comp = self.env.user.company_id.name
        sheet = workbook.add_worksheet('Stock Info')
        format0 = workbook.add_format({'font_size': 20, 'align': 'center', 'bold': True})
        format1 = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold': True})
        format11 = workbook.add_format({'font_size': 12, 'align': 'center', 'bold': True})
        format21 = workbook.add_format({'font_size': 10, 'align': 'center', 'bold': True})
        format3 = workbook.add_format({'bottom': True, 'top': True, 'font_size': 12})
        format4 = workbook.add_format({'font_size': 12, 'align': 'left', 'bold': True})
        font_size_8 = workbook.add_format({'font_size': 8, 'align': 'center'})
        font_size_8_l = workbook.add_format({'font_size': 8, 'align': 'left'})
        font_size_8_r = workbook.add_format({'font_size': 8, 'align': 'right'})
        red_mark = workbook.add_format({'font_size': 8, 'bg_color': 'red'})
        justify = workbook.add_format({'font_size': 12})
        format3.set_align('center')
        justify.set_align('justify')
        format1.set_align('center')
        red_mark.set_align('center')
        sheet.merge_range(1, 3, 2, 7, 'Invoice Outstanding Report', format0)
        # sheet.merge_range(4, 4, 2, 7, comp, format11)
        sheet.set_column(10, 0, 20)
        sheet.set_column(10, 1, 20)
        sheet.set_column(10, 2, 20)
        sheet.set_column(10, 3, 20)
        sheet.set_column(10, 4, 20)
        sheet.set_column(10, 5, 20)
        sheet.set_column(10, 6, 20)
        sheet.set_column(10, 7, 20)
        sheet.set_column(10, 8, 20)
        sheet.set_column(10, 9, 20)

        # sheet.col(0).width = 20
        # sheet.col(1).width = 20    
        sheet.merge_range(6, 0, 6, 4, 'From ' + str(lines.start_date) + ' To ' + str(lines.end_date), format4)
        user = self.env['res.users'].browse(self.env.uid)
        tz = pytz.timezone(user.tz)
        time = pytz.utc.localize(datetime.now()).astimezone(tz)
        sheet.merge_range(7,0,7,4, 'Report Date: ' + str(time.strftime("%Y-%m-%d %H:%M %p")), format4)
            
        sheet.write(10,0, 'Customer', format4)
        sheet.write(10,1,'Invoice Date', format4)
        sheet.write(10,2,'Name', format4)
        sheet.write(10,3,'Sales Person', format4)
        sheet.write(10,4,'Due Date', format4)
        sheet.write(10,5,'Total', format4)
        sheet.write(10,6,'Adjusted', format4)
        sheet.write(10,7,'Amount Due', format4)
        sheet.write(10,8,'Due Days', format4)
            
        total_amount_due = 0
        invoices = self.env['account.move'].search([('invoice_date', '>=', lines.start_date),('invoice_date', '<=', lines.end_date),('move_type','=', 'out_invoice'),('state','in',['posted'])])
        if invoices:
            w_col_no = 0
            w_row_no =  11
            amount_due = 0
            for inv in invoices:
                sheet.write(w_row_no,w_col_no,inv.partner_id.name, font_size_8_l)
                sheet.write(w_row_no,w_col_no + 1,str(inv.invoice_date), font_size_8_l)
                sheet.write(w_row_no,w_col_no + 2,inv.name, font_size_8_l)
                sheet.write(w_row_no,w_col_no + 3,inv.user_id.name, font_size_8_l)
                _logger.info('=================date=====%s',inv.invoice_date_due)
                sheet.write(w_row_no,w_col_no + 4,str(inv.invoice_date_due), font_size_8_l)
                sheet.write(w_row_no,w_col_no + 5,inv.amount_total, font_size_8_l)
                adjusted_total = inv.amount_total-inv.amount_residual
                sheet.write(w_row_no,w_col_no + 6,adjusted_total, font_size_8_l)
                sheet.write(w_row_no,w_col_no + 7,inv.amount_residual, font_size_8_l)

                due_days = inv.invoice_date_due-inv.invoice_date
                _logger.info('=================date2=====%s',str(due_days.days))
                
                sheet.write(w_row_no,w_col_no + 8,str(due_days.days) + ' days', font_size_8_l)

                w_row_no += 1
                amount_due += inv.amount_total
            total_amount_due = amount_due
            sheet.merge_range(18, 0, 18, 2, 'The total amount due is:', format11)

            sheet.write(w_row_no + 1,w_col_no + 3,total_amount_due, format4)
                
        else:
            raise UserError('No records found')
        # w_col_no1 = 7
        # w_house = ', '
        # cat = ', '
        # c = []
        # d1 = d.mapped('id')
        # if d1:
        #     for i in d1:
        #         c.append(self.env['product.category'].browse(i).name)
        #     cat = cat.join(c)
        #     sheet.merge_range(4, 0, 4, 1, 'Category(s) : ', format4)
        #     sheet.merge_range(4, 2, 4, 3 + len(d1), cat, format4)
        # sheet.merge_range(5, 0, 5, 1, 'Warehouse(s) : ', format4)
        # w_house = w_house.join(get_warehouse[0])
        # sheet.merge_range(5, 2, 5, 3+len(get_warehouse[0]), w_house, format4)

        # user = self.env['res.users'].browse(self.env.uid)
        # tz = pytz.timezone(user.tz)
        # time = pytz.utc.localize(datetime.now()).astimezone(tz)
        # sheet.merge_range('A8:G8', 'Report Date: ' + str(time.strftime("%Y-%m-%d %H:%M %p")), format1)
            #  <td><span t-field="invoice.partner_id"/></td>
            #                 <td><span t-field="invoice.date_invoice"/></td>
            #                 <td><span t-field="invoice.number"/></td>
            #                 <td><span t-field="invoice.user_id"/></td>
            #                 <td><span t-field="invoice.invoice_date_due"/></td>
            #                 <td><span t-field="invoice.amount_total"/></td>
            #                 <td><t t-set="adjusted_total" t-value="invoice.amount_total-invoice.amount_residual"/>
            #                 <t t-esc="adjusted_total"/>
            #                 </td>
            #                 <td><span t-field="invoice.amount_residual"/></td>
            #                 <td><t t-set="due_days" t-value="invoice.invoice_date_due-invoice.date_invoice"/>
            #                 <span><t t-esc="due_days.days"/> days</span>
            #                 </td>
            user = self.env['res.users'].browse(self.env.uid)
            tz = pytz.timezone(user.tz)
            time = pytz.utc.localize(datetime.now()).astimezone(tz)
            # sheet.merge_range('A8:K8', 'Report Date: ' + str(time.strftime("%Y-%m-%d %H:%M %p")), format1)
            # sheet.merge_range(7, 7, 7, count, 'Warehouses', format1)
            # sheet.merge_range('A9:G9', 'Product Information', format11)
            
            # for i in get_warehouse[0]:
            #     w_col_no = w_col_no + 11
            #     sheet.merge_range(8, w_col_no1, 8, w_col_no, i, format11)
            #     w_col_no1 = w_col_no1 + 11
            # sheet.write( 'Customer', format21)
            # sheet.write(w_col_no,w_row_no + 2,'Invoice Date', format21)
            # sheet.write(w_col_no,w_row_no + 3,'Number', format21)
            # sheet.write(w_col_no,w_row_no + 4,'Sales Person', format21)
            # sheet.write(w_col_no,w_row_no + 5,'Due Date', format21)
            # sheet.write(w_col_no,w_row_no + 6,'Total', format21)
            # sheet.write(w_col_no,w_row_no + 7,'Adjusted', format21)
            # sheet.write(w_col_no,w_row_no + 8,'Amount Due', format21)
            # sheet.write(w_col_no,w_row_no + 9,'Due Days', format21)
            # for inv in invoices:
                # sheet.write(w_col_no,w_row_no,str(inv.date_invoice), format21)
                # sheet.write(w_col_no + 1,w_row_no,str(inv.date_invoice), format21)
                # w_row_no += 1


        # sheet.merge_range(9, 4, 9, 5, 'Category', format21)
        # sheet.write(9, 6, 'Cost Price', format21)
        # p_col_no1 = 7
        # for i in get_warehouse[0]:
        #     sheet.write(9, p_col_no1, 'Available', format21)
        #     sheet.write(9, p_col_no1 + 1, 'Virtual', format21)
        #     sheet.write(9, p_col_no1 + 2, 'Incoming', format21)
        #     sheet.write(9, p_col_no1 + 3, 'Outgoing', format21)
        #     sheet.merge_range(9, p_col_no1 + 4, 9, p_col_no1 + 5, 'Net On Hand', format21)
        #     sheet.merge_range(9, p_col_no1 + 6, 9, p_col_no1 + 7, 'Total Sold', format21)
        #     sheet.merge_range(9, p_col_no1 + 8, 9, p_col_no1 + 9, 'Total Purchased', format21)
        #     sheet.write(9, p_col_no1 + 10, 'Valuation', format21)
        #     p_col_no1 = p_col_no1 + 11
        # prod_row = 10
        # prod_col = 0
        # for i in get_warehouse[1]:
        #     get_line = self.get_lines(d, i)
        #     for each in get_line:
        #         sheet.write(prod_row, prod_col, each['sku'], font_size_8)
        #         sheet.merge_range(prod_row, prod_col + 1, prod_row, prod_col + 3, each['name'], font_size_8_l)
        #         sheet.merge_range(prod_row, prod_col + 4, prod_row, prod_col + 5, each['category'], font_size_8_l)
        #         sheet.write(prod_row, prod_col + 6, each['cost_price'], font_size_8_r)
        #         prod_row = prod_row + 1
        #     break
        # prod_row = 10
        # prod_col = 7
        # for i in get_warehouse[1]:
        #     get_line = self.get_lines(d, i)
        #     for each in get_line:
        #         if each['available'] < 0:
        #             sheet.write(prod_row, prod_col, each['available'], red_mark)
        #         else:
        #             sheet.write(prod_row, prod_col, each['available'], font_size_8)
        #         if each['virtual'] < 0:
        #             sheet.write(prod_row, prod_col + 1, each['virtual'], red_mark)
        #         else:
        #             sheet.write(prod_row, prod_col + 1, each['virtual'], font_size_8)
        #         if each['incoming'] < 0:
        #             sheet.write(prod_row, prod_col + 2, each['incoming'], red_mark)
        #         else:
        #             sheet.write(prod_row, prod_col + 2, each['incoming'], font_size_8)
        #         if each['outgoing'] < 0:
        #             sheet.write(prod_row, prod_col + 3, each['outgoing'], red_mark)
        #         else:
        #             sheet.write(prod_row, prod_col + 3, each['outgoing'], font_size_8)
        #         if each['net_on_hand'] < 0:
        #             sheet.merge_range(prod_row, prod_col + 4, prod_row, prod_col + 5, each['net_on_hand'], red_mark)
        #         else:
        #             sheet.merge_range(prod_row, prod_col + 4, prod_row, prod_col + 5, each['net_on_hand'], font_size_8)
        #         if each['sale_value'] < 0:
        #             sheet.merge_range(prod_row, prod_col + 6, prod_row, prod_col + 7, each['sale_value'], red_mark)
        #         else:
        #             sheet.merge_range(prod_row, prod_col + 6, prod_row, prod_col + 7, each['sale_value'], font_size_8)
        #         if each['purchase_value'] < 0:
        #             sheet.merge_range(prod_row, prod_col + 8, prod_row, prod_col + 9, each['purchase_value'], red_mark)
        #         else:
        #             sheet.merge_range(prod_row, prod_col + 8, prod_row, prod_col + 9, each['purchase_value'], font_size_8)
        #         if each['total_value'] < 0:
        #             sheet.write(prod_row, prod_col + 10, each['total_value'], red_mark)
        #         else:
        #             sheet.write(prod_row, prod_col + 10, each['total_value'], font_size_8_r)
        #         prod_row = prod_row + 1
        #     prod_row = 10
        #     prod_col = prod_col + 11
        #     # continue

     