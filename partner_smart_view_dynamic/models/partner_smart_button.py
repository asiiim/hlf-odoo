# -*- coding: utf-8 -*-


from odoo import api, fields, models,_
import time

import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import AccessError, UserError, AccessDenied
from odoo.tools import date_utils
import json
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter
import io
FETCH_RANGE = 2000
DATE_DICT = {
    '%m/%d/%Y' : 'mm/dd/yyyy',
    '%Y/%m/%d' : 'yyyy/mm/dd',
    '%m/%d/%y' : 'mm/dd/yy',
    '%d/%m/%Y' : 'dd/mm/yyyy',
    '%d/%m/%y' : 'dd/mm/yy',
    '%d-%m-%Y' : 'dd-mm-yyyy',
    '%d-%m-%y' : 'dd-mm-yy',
    '%m-%d-%Y' : 'mm-dd-yyyy',
    '%m-%d-%y' : 'mm-dd-yy',
    '%Y-%m-%d' : 'yyyy-mm-dd',
    '%f/%e/%Y' : 'm/d/yyyy',
    '%f/%e/%y' : 'm/d/yy',
    '%e/%f/%Y' : 'd/m/yyyy',
    '%e/%f/%y' : 'd/m/yy',
    '%f-%e-%Y' : 'm-d-yyyy',
    '%f-%e-%y' : 'm-d-yy',
    '%e-%f-%Y' : 'd-m-yyyy',
    '%e-%f-%y' : 'd-m-yy'
}

class AccountMoveLineInherit(models.Model):
    _inherit = "account.move.line"

         # Nepali Date field
    # nepali_date_ins = fields.Char('Date (B.S.)', compute="_get_nepalidate_mat", store=True)
    nepali_date_ins = fields.Char('Date (B.S.)', compute="_get_nepalidate_ins", store=True)

    @api.depends('date')
    def _get_nepalidate_ins(self):
        dt_format = '%Y-%m-%d'
        for jrnl in self:
            if jrnl.date:
                np_dt_abs = self.env['np.date']
                dt = np_dt_abs.get_nepalidate(str(jrnl.date), dt_format)
                jrnl.update({'nepali_date_ins': dt})


class InsPartLedgerInherit(models.TransientModel):
    _inherit = 'ins.partner.ledger'

    # def validate_data(self):
    #     if self.date_from > self.date_to:
    #         raise ValidationError(_('"Date from" must be less than or equal to "Date to"'))
    #     return True

    def process_filters(self,active_id=None):
        ''' To show on report headers'''

        data = self.get_filters(active_id)

        _logger.info("===========data========%s",data)

        filters = {}
        if data.get('display_accounts') == 'balance_not_zero':
            filters['display_accounts'] = 'With balance not Zero'
        if data.get('balance_less_than_zero'):
            filters['display_accounts'] = 'With balance less than Zero'
        if data.get('balance_greater_than_zero'):
            filters['display_accounts'] = 'With balance greater than Zero'
        else:
            filters['display_accounts'] = 'All'
        if data.get('journal_ids', []):
            filters['journals'] = self.env['account.journal'].browse(data.get('journal_ids', [])).mapped('code')
        else:
            filters['journals'] = ['All']
        if data.get('account_ids', []):
            filters['accounts'] = self.env['account.account'].browse(data.get('account_ids', [])).mapped('code')
        else:
            filters['accounts'] = ['All']

        if data.get('partner_ids', []):
            filters['partners'] = self.env['res.partner'].browse(data.get('partner_ids', [])).mapped('name')
        else:
            filters['partners'] = ['All']

        if data.get('partner_category_ids', []):
            filters['categories'] = self.env['res.partner.category'].browse(data.get('partner_category_ids', [])).mapped('name')
        else:
            filters['categories'] = ['All']

        if data.get('target_moves') == 'all_entries':
            filters['target_moves'] = 'All Entries'
        else:
            filters['target_moves'] = 'Posted Only'

        if data.get('date_from', False):
            filters['date_from'] = data.get('date_from')
        if data.get('date_to', False):
            filters['date_to'] = data.get('date_to')

        if data.get('initial_balance'):
            filters['initial_balance'] = 'Yes'
        else:
            filters['initial_balance'] = 'No'

        filters['reconciled'] = '-'
        if data.get('reconciled') == 'reconciled':
            filters['reconciled'] = 'Yes'
        if data.get('reconciled') == 'unreconciled':
            filters['reconciled'] = 'No'

        if data.get('company_id'):
            filters['company_id'] = data.get('company_id')
        else:
            filters['company_id'] = ''

        if data.get('include_details'):
            filters['include_details'] = True
        else:
            filters['include_details'] = False

        filters['journals_list'] = data.get('journals_list')
        filters['accounts_list'] = data.get('accounts_list')
        # custom code
        if data.get('active_id'):
            filters['active_id'] = data.get('active_id')
            partobj = self.env['res.partner'].browse(data.get('active_id'))
            filters['partners_list'] = [(partobj.id,partobj.name)]
        else:
            filters['partners_list'] = data.get('partners_list')
            # 
        filters['category_list'] = data.get('category_list')
        filters['company_name'] = data.get('company_name')

        return filters

    def build_where_clause(self, data=False):
        if not data:
            data = self.get_filters()

        if data:

            WHERE = '(1=1)'

            type = ('receivable', 'payable')
            if self.type:
                type = tuple([self.type, 'none'])

            WHERE += ' AND ty.type IN %s' % str(type)

            if data.get('reconciled') == 'reconciled':
                WHERE += ' AND l.amount_residual = 0'
            if data.get('reconciled') == 'unreconciled':
                WHERE += ' AND l.amount_residual != 0'

            if data.get('journal_ids', []):
                WHERE += ' AND j.id IN %s' % str(tuple(data.get('journal_ids')) + tuple([0]))

            if data.get('account_ids', []):
                WHERE += ' AND a.id IN %s' % str(tuple(data.get('account_ids')) + tuple([0]))

            if data.get('partner_ids', []):
                WHERE += ' AND p.id IN %s' % str(tuple(data.get('partner_ids')) + tuple([0]))

            if data.get('company_id', False):
                WHERE += ' AND l.company_id = %s' % data.get('company_id')

            if data.get('target_moves') == 'posted_only':
                WHERE += " AND m.state = 'posted'"

            return WHERE

    def build_detailed_move_lines(self, offset=0, partner=0, fetch_range=FETCH_RANGE):
        '''
        It is used for showing detailed move lines as sub lines. It is defered loading compatable
        :param offset: It is nothing but page numbers. Multiply with fetch_range to get final range
        :param partner: Integer - Partner_id
        :param fetch_range: Global Variable. Can be altered from calling model
        :return: count(int-Total rows without offset), offset(integer), move_lines(list of dict)

        Three sections,
        1. Initial Balance
        2. Current Balance
        3. Final Balance
        '''
        cr = self.env.cr
        data = self.get_filters()
        offset_count = offset * fetch_range
        count = 0
        opening_balance = 0

        currency_id = self.env.company.currency_id

        WHERE = self.build_where_clause()

        WHERE_INIT = WHERE + " AND l.date < '%s'" % data.get('date_from')
        WHERE_INIT += " AND l.partner_id = %s" % partner

        WHERE_CURRENT = WHERE + " AND l.date >= '%s'" % data.get('date_from') + " AND l.date <= '%s'" % data.get(
            'date_to')
        WHERE_CURRENT += " AND p.id = %s" % partner

        if data.get('initial_balance'):
            WHERE_FULL = WHERE + " AND l.date <= '%s'" % data.get('date_to')
        else:
            WHERE_FULL = WHERE + " AND l.date >= '%s'" % data.get('date_from') + " AND l.date <= '%s'" % data.get(
                'date_to')
        WHERE_FULL += " AND p.id = %s" % partner

        ORDER_BY_CURRENT = 'l.date'

        move_lines = []
        if data.get('initial_balance'):
            sql = ('''
                    SELECT 
                        COALESCE(SUM(l.debit),0) AS debit, 
                        COALESCE(SUM(l.credit),0) AS credit, 
                        COALESCE(SUM(l.debit - l.credit),0) AS balance
                    FROM account_move_line l
                    JOIN account_move m ON (l.move_id=m.id)
                    JOIN account_account a ON (l.account_id=a.id)
                    LEFT JOIN account_account_type AS ty ON a.user_type_id = ty.id
                    --LEFT JOIN account_analytic_account anl ON (l.analytic_account_id=anl.id)
                    LEFT JOIN res_currency c ON (l.currency_id=c.id)
                    LEFT JOIN res_partner p ON (l.partner_id=p.id)
                    JOIN account_journal j ON (l.journal_id=j.id)
                    WHERE %s
                ''') % WHERE_INIT
            cr.execute(sql)
            row = cr.dictfetchone()
            opening_balance += row.get('balance')

        sql = ('''
                    SELECT 
                        COALESCE(SUM(l.debit - l.credit),0) AS balance
                    FROM account_move_line l
                    JOIN account_move m ON (l.move_id=m.id)
                    JOIN account_account a ON (l.account_id=a.id)
                    LEFT JOIN account_account_type AS ty ON a.user_type_id = ty.id
                    --LEFT JOIN account_analytic_account anl ON (l.analytic_account_id=anl.id)
                    LEFT JOIN res_currency c ON (l.currency_id=c.id)
                    LEFT JOIN res_currency cc ON (l.company_currency_id=cc.id)
                    LEFT JOIN res_partner p ON (l.partner_id=p.id)
                    JOIN account_journal j ON (l.journal_id=j.id)
                    WHERE %s
                    GROUP BY l.date, l.move_id
                    ORDER BY %s
                    OFFSET %s ROWS
                    FETCH FIRST %s ROWS ONLY
                ''') % (WHERE_CURRENT, ORDER_BY_CURRENT, 0, offset_count)
        cr.execute(sql)
        running_balance_list = cr.fetchall()
        for running_balance in running_balance_list:
            opening_balance += running_balance[0]
        sql = ('''
            SELECT COUNT(*)
            FROM account_move_line l
                JOIN account_move m ON (l.move_id=m.id)
                JOIN account_account a ON (l.account_id=a.id)
                LEFT JOIN account_account_type AS ty ON a.user_type_id = ty.id
                --LEFT JOIN account_analytic_account anl ON (l.analytic_account_id=anl.id)
                LEFT JOIN res_currency c ON (l.currency_id=c.id)
                LEFT JOIN res_currency cc ON (l.company_currency_id=cc.id)
                LEFT JOIN res_partner p ON (l.partner_id=p.id)
                JOIN account_journal j ON (l.journal_id=j.id)
            WHERE %s
        ''')% (WHERE_CURRENT)
        cr.execute(sql)
        count = cr.fetchone()[0]
        if (int(offset_count / fetch_range) == 0) and data.get('initial_balance'):
            sql = ('''
                    SELECT 
                        COALESCE(SUM(l.debit),0) AS debit, 
                        COALESCE(SUM(l.credit),0) AS credit, 
                        COALESCE(SUM(l.debit - l.credit),0) AS balance
                    FROM account_move_line l
                    JOIN account_move m ON (l.move_id=m.id)
                    JOIN account_account a ON (l.account_id=a.id)
                    LEFT JOIN account_account_type AS ty ON a.user_type_id = ty.id
                    --LEFT JOIN account_analytic_account anl ON (l.analytic_account_id=anl.id)
                    LEFT JOIN res_currency c ON (l.currency_id=c.id)
                    LEFT JOIN res_partner p ON (l.partner_id=p.id)
                    JOIN account_journal j ON (l.journal_id=j.id)
                    WHERE %s
                ''') % WHERE_INIT
            cr.execute(sql)
            for row in cr.dictfetchall():
                row['move_name'] = 'Initial Balance'
                row['partner_id'] = partner
                row['company_currency_id'] = currency_id.id
                move_lines.append(row)
        sql = ('''
                SELECT
                    l.id AS lid,
                    l.account_id AS account_id,
                    l.partner_id AS partner_id,
                    l.date AS ldate,
                    l.nepali_date_ins as nepali_date_ins,
                    j.code AS lcode,
                    l.currency_id,
                    l.amount_currency,
                    --l.ref AS lref,
                    l.name AS lname,
                    m.id AS move_id,
                    m.name AS move_name,
                    c.symbol AS currency_symbol,
                    c.position AS currency_position,
                    c.rounding AS currency_precision,
                    cc.id AS company_currency_id,
                    cc.symbol AS company_currency_symbol,
                    cc.rounding AS company_currency_precision,
                    cc.position AS company_currency_position,
                    p.name AS partner_name,
                    a.name AS account_name,
                    COALESCE(l.debit,0) AS debit,
                    COALESCE(l.credit,0) AS credit,
                    COALESCE(l.debit - l.credit,0) AS balance,
                    COALESCE(l.amount_currency,0) AS amount_currency
                FROM account_move_line l
                JOIN account_move m ON (l.move_id=m.id)
                JOIN account_account a ON (l.account_id=a.id)
                LEFT JOIN account_account_type AS ty ON a.user_type_id = ty.id
                --LEFT JOIN account_analytic_account anl ON (l.analytic_account_id=anl.id)
                LEFT JOIN res_currency c ON (l.currency_id=c.id)
                LEFT JOIN res_currency cc ON (l.company_currency_id=cc.id)
                LEFT JOIN res_partner p ON (l.partner_id=p.id)
                JOIN account_journal j ON (l.journal_id=j.id)
                WHERE %s
                GROUP BY l.id, l.partner_id, a.name, l.account_id, l.date, j.code, l.currency_id, l.amount_currency, l.name, m.id, m.name, c.rounding, cc.id, cc.rounding, cc.position, c.position, c.symbol, cc.symbol, p.name
                ORDER BY %s
                OFFSET %s ROWS
                FETCH FIRST %s ROWS ONLY
            ''') % (WHERE_CURRENT, ORDER_BY_CURRENT, offset_count, fetch_range)
        cr.execute(sql)

        for row in cr.dictfetchall():
            row['ldatenep'] = str(row['ldate']) + " (" + row['nepali_date_ins'] + ")"
            current_balance = row['balance']
            row['balance'] = opening_balance + current_balance
            opening_balance += current_balance
            row['initial_bal'] = False
            move_lines.append(row)

        if ((count - offset_count) <= fetch_range) and data.get('initial_balance'):
            sql = ('''
                    SELECT 
                        COALESCE(SUM(l.debit),0) AS debit, 
                        COALESCE(SUM(l.credit),0) AS credit, 
                        COALESCE(SUM(l.debit - l.credit),0) AS balance
                    FROM account_move_line l
                    JOIN account_move m ON (l.move_id=m.id)
                    JOIN account_account a ON (l.account_id=a.id)
                    LEFT JOIN account_account_type AS ty ON a.user_type_id = ty.id
                    --LEFT JOIN account_analytic_account anl ON (l.analytic_account_id=anl.id)
                    LEFT JOIN res_currency c ON (l.currency_id=c.id)
                    LEFT JOIN res_partner p ON (l.partner_id=p.id)
                    JOIN account_journal j ON (l.journal_id=j.id)
                    WHERE %s
                ''') % WHERE_FULL
            cr.execute(sql)
            for row in cr.dictfetchall():
                row['move_name'] = 'Ending Balance'
                row['partner_id'] = partner
                row['company_currency_id'] = currency_id.id
                move_lines.append(row)
        return count, offset_count, move_lines

    def process_data(self,active_id=None):
        '''
        It is the method for showing summary details of each accounts. Just basic details to show up
        Three sections,
        1. Initial Balance
        2. Current Balance
        3. Final Balance
        :return:
        '''
        cr = self.env.cr

        data = self.get_filters(active_id)

        WHERE = self.build_where_clause(data)

        partner_company_domain = [('parent_id', '=', False),
                                  '|',
                                  ('customer_rank', '>', 0),
                                  ('supplier_rank', '>', 0),
                                  '|',
                                  ('company_id', '=', self.env.company.id),
                                  ('company_id', '=', False)]
        if self.partner_category_ids:
            partner_company_domain.append(('category_id','in',self.partner_category_ids.ids))

        if data.get('partner_ids', []):
            partner_ids = self.env['res.partner'].browse(data.get('partner_ids'))
        else:
            partner_ids = self.env['res.partner'].search(partner_company_domain)

        move_lines = {
            x.id: {
                'name': x.name,
                'code': x.id,
                'company_currency_id': 0,
                'company_currency_symbol': 'AED',
                'company_currency_precision': 0.0100,
                'company_currency_position': 'after',
                'id': x.id,
                'lines': []
            } for x in partner_ids
        }
        for partner in partner_ids:

            currency = partner.company_id.currency_id or self.env.company.currency_id
            symbol = currency.symbol
            rounding = currency.rounding
            position = currency.position

            opening_balance = 0.0

            WHERE_INIT = WHERE + " AND l.date < '%s'" % data.get('date_from')
            WHERE_INIT += " AND l.partner_id = %s" % partner.id
            ORDER_BY_CURRENT = 'l.date'

            if data.get('initial_balance'):
                sql = ('''
                    SELECT 
                        COALESCE(SUM(l.debit),0) AS debit, 
                        COALESCE(SUM(l.credit),0) AS credit, 
                        COALESCE(SUM(l.debit - l.credit),0) AS balance
                    FROM account_move_line l
                    JOIN account_move m ON (l.move_id=m.id)
                    JOIN account_account a ON (l.account_id=a.id)
                    LEFT JOIN account_account_type AS ty ON a.user_type_id = ty.id
                    --LEFT JOIN account_analytic_account anl ON (l.analytic_account_id=anl.id)
                    LEFT JOIN res_currency c ON (l.currency_id=c.id)
                    LEFT JOIN res_partner p ON (l.partner_id=p.id)
                    JOIN account_journal j ON (l.journal_id=j.id)
                    WHERE %s
                ''') % WHERE_INIT
                cr.execute(sql)
                for row in cr.dictfetchall():
                    row['move_name'] = 'Initial Balance'
                    row['partner_id'] = partner.id
                    row['initial_bal'] = True
                    row['ending_bal'] = False
                    opening_balance += row['balance']
                    move_lines[partner.id]['lines'].append(row)
            WHERE_CURRENT = WHERE + " AND l.date >= '%s'" % data.get('date_from') + " AND l.date <= '%s'" % data.get(
                'date_to')
            WHERE_CURRENT += " AND p.id = %s" % partner.id
            sql = ('''
                SELECT
                    l.id AS lid,
                    l.date AS ldate,
                    l.nepali_date_ins AS nepali_date_ins,
                    j.code AS lcode,
                    a.name AS account_name,
                    m.name AS move_name,
                    l.name AS lname,
                    COALESCE(l.debit,0) AS debit,
                    COALESCE(l.credit,0) AS credit,
                    COALESCE(l.balance,0) AS balance,
                    COALESCE(l.amount_currency,0) AS balance_currency
                FROM account_move_line l
                JOIN account_move m ON (l.move_id=m.id)
                JOIN account_account a ON (l.account_id=a.id)
                LEFT JOIN account_account_type AS ty ON a.user_type_id = ty.id
                --LEFT JOIN account_analytic_account anl ON (l.analytic_account_id=anl.id)
                LEFT JOIN res_currency c ON (l.currency_id=c.id)
                LEFT JOIN res_currency cc ON (l.company_currency_id=cc.id)
                LEFT JOIN res_partner p ON (l.partner_id=p.id)
                JOIN account_journal j ON (l.journal_id=j.id)
                WHERE %s
                --GROUP BY l.id, l.account_id, l.date, j.code, l.currency_id, l.amount_currency, l.ref, l.name, m.id, m.name, c.rounding, cc.rounding, cc.position, c.position, c.symbol, cc.symbol, p.name
                ORDER BY %s
            ''') % (WHERE_CURRENT, ORDER_BY_CURRENT)
            cr.execute(sql)
            current_lines = cr.dictfetchall()
            for row in current_lines:
                row['ldatenep'] = str(row['ldate']) + " (" + row['nepali_date_ins'] + ")"
                row['initial_bal'] = False
                row['ending_bal'] = False

                current_balance = row['balance']
                # row['balance'] = opening_balance + current_balance
                if row['balance'] > 0:
                    row['balance'] = "Rs " + str(opening_balance) + str(current_balance) + " Dr"
                elif row['balance'] == 0:
                    row['balance'] = "Rs " + str(opening_balance) + str(current_balance) 
                else:
                    row['balance'] = "Rs " + str(abs(opening_balance)) + str(abs(current_balance)) + " Cr"
                _logger.info("=========================================abcdeee==============%s",row['balance'])

                opening_balance += current_balance
                row['initial_bal'] = False

                move_lines[partner.id]['lines'].append(row)
            if data.get('initial_balance'):
                WHERE_FULL = WHERE + " AND l.date <= '%s'" % data.get('date_to')
            else:
                WHERE_FULL = WHERE + " AND l.date >= '%s'" % data.get('date_from') + " AND l.date <= '%s'" % data.get(
                    'date_to')
            WHERE_FULL += " AND p.id = %s" % partner.id
            sql = ('''
                SELECT 
                    COALESCE(SUM(l.debit),0) AS debit, 
                    COALESCE(SUM(l.credit),0) AS credit, 
                    COALESCE(SUM(l.debit - l.credit),0) AS balance
                FROM account_move_line l
                JOIN account_move m ON (l.move_id=m.id)
                JOIN account_account a ON (l.account_id=a.id)
                LEFT JOIN account_account_type AS ty ON a.user_type_id = ty.id
                --LEFT JOIN account_analytic_account anl ON (l.analytic_account_id=anl.id)
                LEFT JOIN res_currency c ON (l.currency_id=c.id)
                LEFT JOIN res_partner p ON (l.partner_id=p.id)
                JOIN account_journal j ON (l.journal_id=j.id)
                WHERE %s
            ''') % WHERE_FULL
            cr.execute(sql)
            for row in cr.dictfetchall():
                if (data.get('display_accounts') == 'balance_not_zero' and currency.is_zero(row['debit'] - row['credit']))\
                        or (data.get('balance_less_than_zero') and (row['debit'] - row['credit']) > 0)\
                        or (data.get('balance_greater_than_zero') and (row['debit'] - row['credit']) < 0):
                    move_lines.pop(partner.id, None)
                else:
                    row['ending_bal'] = True
                    row['initial_bal'] = False
                    move_lines[partner.id]['lines'].append(row)
                    move_lines[partner.id]['debit'] = row['debit']
                    move_lines[partner.id]['credit'] = row['credit']
                    move_lines[partner.id]['balance'] = row['balance']
                    move_lines[partner.id]['company_currency_id'] = currency.id
                    move_lines[partner.id]['company_currency_symbol'] = symbol
                    move_lines[partner.id]['company_currency_precision'] = rounding
                    move_lines[partner.id]['company_currency_position'] = position
                    move_lines[partner.id]['count'] = len(current_lines)
                    move_lines[partner.id]['pages'] = self.get_page_list(len(current_lines))
                    move_lines[partner.id]['single_page'] = True if len(current_lines) <= FETCH_RANGE else False
        return move_lines

    def get_page_list(self, total_count):
        '''
        Helper function to get list of pages from total_count
        :param total_count: integer
        :return: list(pages) eg. [1,2,3,4,5,6,7 ....]
        '''
        page_count = int(total_count / FETCH_RANGE)
        if total_count % FETCH_RANGE:
            page_count += 1
        return [i+1 for i in range(0, int(page_count))] or []

    def get_filters(self,active_id=None):

        self.onchange_date_range()

        company_domain = [('company_id', '=', self.env.company.id)]
        partner_company_domain = [('parent_id','=', False),
                                  '|',
                                  ('customer_rank', '>', 0),
                                  ('supplier_rank', '>', 0),
                                  '|',
                                  ('company_id', '=', self.env.company.id),
                                  ('company_id', '=', False)]

        journals = self.journal_ids if self.journal_ids else self.env['account.journal'].search(company_domain)
        accounts = self.account_ids if self.account_ids else self.env['account.account'].search(company_domain)
        # partners = self.partner_ids if self.partner_ids else self.env['res.partner'].search(partner_company_domain)
        # custom code below
        if active_id:
            _logger.info("hereeeeeeeeeeeeeee")
            partner = self.env['res.partner'].search([('id','in',active_id)])
            _logger.info("hereeeeeeeeeeeeeee%s",partner)
            partners = partner
            
        else:
            _logger.info("===========there=======")
            partners = self.partner_ids if self.partner_ids else self.env['res.partner'].search(partner_company_domain)

        categories = self.partner_category_ids if self.partner_category_ids else self.env['res.partner.category'].search([])

        filter_dict = {
            'journal_ids': self.journal_ids.ids,
            'account_ids': self.account_ids.ids,
            'partner_ids': self.partner_ids.ids,
            'partner_category_ids': self.partner_category_ids.ids,
            'company_id': self.company_id and self.company_id.id or False,
            'target_moves': self.target_moves,
            'initial_balance': self.initial_balance,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'reconciled': self.reconciled,
            'display_accounts': self.display_accounts,
            'include_details': self.include_details,
            'balance_less_than_zero': self.balance_less_than_zero,
            'balance_greater_than_zero': self.balance_greater_than_zero,
            'journals_list': [(j.id, j.name) for j in journals],
            'accounts_list': [(a.id, a.name) for a in accounts],
            'partners_list': [(p.id, p.name) for p in partners],
            'category_list': [(c.id, c.name) for c in categories],
            'company_name': self.company_id and self.company_id.name,
        }
        if active_id:
            filter_dict['active_id'] = active_id[0]

        default_filters = {}
        filter_dict.update(default_filters)
        # _logger.info("================aaaaaa=%s",filter_dict['active_id'])
        return filter_dict

    def get_report_datas(self,active_id=None):
        '''
        Main method for pdf, xlsx and js calls
        :param default_filters: Use this while calling from other methods. Just a dict
        :return: All the datas for GL
        '''
        _logger.info("============act========%s",active_id)
        if self.validate_data():
            filters = self.process_filters(active_id)
            account_lines = self.process_data(active_id)
            return filters, account_lines
    def write(self, vals):

        if vals.get('date_range'):
            vals.update({'date_from': False, 'date_to': False})
        if vals.get('date_from') and vals.get('date_to'):
            vals.update({'date_range': False})

        if vals.get('journal_ids'):
            vals.update({'journal_ids': vals.get('journal_ids')})
        if vals.get('journal_ids') == []:
            vals.update({'journal_ids': [(5,)]})

        if vals.get('account_ids'):
            vals.update({'account_ids': vals.get('account_ids')})
        if vals.get('account_ids') == []:
            vals.update({'account_ids': [(5,)]})
        _logger.info("===========pids=====%s",vals.get('partner_ids'))
        if vals.get('partner_ids'):
            vals.update({'partner_ids': vals.get('partner_ids')})
        if vals.get('partner_ids') == []:
            vals.update({'partner_ids': [(5,)]})

        if vals.get('partner_category_ids'):
            vals.update({'partner_category_ids': vals.get('partner_category_ids')})
        if vals.get('partner_category_ids') == []:
            vals.update({'partner_category_ids': [(5,)]})

        ret = super(InsPartLedgerInherit, self).write(vals)
        return ret

    # def action_pdf(self):
    #     filters, account_lines = self.get_report_datas()
    #     return self.env.ref(
    #         'account_dynamic_reports'
    #         '.action_print_partner_ledger').report_action(
    #         self, data={'Ledger_data': account_lines,
    #                     'Filters': filters
    #                     })

    # def action_xlsx(self):
    #     ''' Button function for Xlsx '''

    #     data = self.read()
    #     date_from = fields.Date.from_string(self.date_from).strftime(
    #         self.env['res.lang'].search([('code', '=', self.env.user.lang)])[0].date_format)
    #     date_to = fields.Date.from_string(self.date_to).strftime(
    #         self.env['res.lang'].search([('code', '=', self.env.user.lang)])[0].date_format)

    #     return {
    #         'type': 'ir.actions.report',
    #         'data': {'model': 'ins.partner.ledger',
    #                  'options': json.dumps(data[0], default=date_utils.json_default),
    #                  'output_format': 'xlsx',
    #                  'report_name': 'Partner Ledger - %s-%s' % (date_from, date_to),
    #                  },
    #         'report_type': 'xlsx'
    #     }

    def get_xlsx_report(self, data, response):
        # Initialize
        #############################################################
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Partner Ledger')
        sheet.set_zoom(95)
        sheet_2 = workbook.add_worksheet('Filters')
        sheet_2.protect()

        # Get record and data
        record = self.env['ins.partner.ledger'].browse(data.get('id', [])) or False
        filter, account_lines = record.get_report_datas()

        # Formats
        ############################################################
        sheet.set_column(0, 0, 12)
        sheet.set_column(1, 1, 12)
        sheet.set_column(2, 2, 30)
        sheet.set_column(3, 3, 18)
        sheet.set_column(4, 4, 30)
        sheet.set_column(5, 5, 13)
        sheet.set_column(6, 6, 13)
        sheet.set_column(7, 7, 13)

        sheet_2.set_column(0, 0, 35)
        sheet_2.set_column(1, 1, 25)
        sheet_2.set_column(2, 2, 25)
        sheet_2.set_column(3, 3, 25)
        sheet_2.set_column(4, 4, 25)
        sheet_2.set_column(5, 5, 25)
        sheet_2.set_column(6, 6, 25)

        sheet.freeze_panes(4, 0)

        sheet.screen_gridlines = False
        sheet_2.screen_gridlines = False
        sheet_2.protect()

        format_title = workbook.add_format({
            'bold': True,
            'align': 'center',
            'font_size': 12,
            'font': 'Arial',
            'border': False
        })
        format_header = workbook.add_format({
            'bold': True,
            'font_size': 10,
            'align': 'center',
            'font': 'Arial',
            # 'border': True
        })
        content_header = workbook.add_format({
            'bold': False,
            'font_size': 10,
            'align': 'center',
            'border': True,
            'font': 'Arial',
        })
        content_header_date = workbook.add_format({
            'bold': False,
            'font_size': 10,
            'border': True,
            'align': 'center',
            'font': 'Arial',
        })
        line_header = workbook.add_format({
            'bold': True,
            'font_size': 10,
            'align': 'center',
            'top': True,
            'bottom': True,
            'font': 'Arial',
        })
        line_header_light = workbook.add_format({
            'bold': False,
            'font_size': 10,
            'align': 'center',
            'text_wrap': True,
            'font': 'Arial',
            'valign': 'top'
        })
        line_header_light_date = workbook.add_format({
            'bold': False,
            'font_size': 10,
            'align': 'center',
            'font': 'Arial',
        })
        line_header_light_initial = workbook.add_format({
            'italic': True,
            'font_size': 10,
            'align': 'center',
            'bottom': True,
            'font': 'Arial',
            'valign': 'top'
        })
        line_header_light_initial_bold = workbook.add_format({
            'bold': True,
            'italic': True,
            'font_size': 10,
            'align': 'center',
            'bottom': True,
            'font': 'Arial',
            'valign': 'top'
        })
        line_header_light_ending = workbook.add_format({
            'italic': True,
            'font_size': 10,
            'align': 'center',
            'top': True,
            'font': 'Arial',
            'valign': 'top'
        })
        line_header_light_ending_bold = workbook.add_format({
            'bold': True,
            'italic': True,
            'font_size': 10,
            'align': 'center',
            'bottom': True,
            'font': 'Arial',
            'valign': 'top'
        })
        lang = self.env.user.lang
        lang_id = self.env['res.lang'].search([('code', '=', lang)])[0]
        currency_id = self.env.user.company_id.currency_id
        line_header.num_format = currency_id.excel_format
        line_header_light.num_format = currency_id.excel_format
        line_header_light_initial.num_format = currency_id.excel_format
        line_header_light_ending.num_format = currency_id.excel_format
        line_header_light_date.num_format = DATE_DICT.get(lang_id.date_format, 'dd/mm/yyyy')
        content_header_date.num_format = DATE_DICT.get(lang_id.date_format, 'dd/mm/yyyy')

        # Write data
        ################################################################
        row_pos_2 = 0
        row_pos = 0
        sheet.merge_range(0, 0, 0, 8, 'Partner Ledger' + ' - ' + data['company_id'][1], format_title)

        # Write filters
        sheet_2.write(row_pos_2, 0, _('Date from'), format_header)
        datestring = fields.Date.from_string(str(filter['date_from'])).strftime(lang_id.date_format)
        sheet_2.write(row_pos_2, 1, datestring or '', content_header_date)
        row_pos_2 += 1
        sheet_2.write(row_pos_2, 0, _('Date to'), format_header)
        datestring = fields.Date.from_string(str(filter['date_to'])).strftime(lang_id.date_format)
        sheet_2.write(row_pos_2, 1, datestring or '', content_header_date)
        row_pos_2 += 1
        sheet_2.write(row_pos_2, 0, _('Target moves'), format_header)
        sheet_2.write(row_pos_2, 1, filter['target_moves'], content_header)
        row_pos_2 += 1
        sheet_2.write(row_pos_2, 0, _('Display accounts'), format_header)
        sheet_2.write(row_pos_2, 1, filter['display_accounts'], content_header)
        row_pos_2 += 1
        sheet_2.write(row_pos_2, 0, _('Reconciled'), format_header)
        sheet_2.write(row_pos_2, 1, filter['reconciled'], content_header)
        row_pos_2 += 1
        sheet_2.write(row_pos_2, 0, _('Initial Balance'), format_header)
        sheet_2.write(row_pos_2, 1, filter['initial_balance'], content_header)
        row_pos_2 += 1
        # Journals
        row_pos_2 += 2
        sheet_2.write(row_pos_2, 0, _('Journals'), format_header)
        j_list = ', '.join([lt or '' for lt in filter.get('journals')])
        sheet_2.write(row_pos_2, 1, j_list, content_header)
        # Partners
        row_pos_2 += 1
        sheet_2.write(row_pos_2, 0, _('Partners'), format_header)
        p_list = ', '.join([lt or '' for lt in filter.get('partners')])
        sheet_2.write(row_pos_2, 1, p_list, content_header)
        # Partner Tags
        row_pos_2 += 1
        sheet_2.write(row_pos_2, 0, _('Partner Tag'), format_header)
        p_list = ', '.join([lt or '' for lt in filter.get('categories')])
        sheet_2.write(row_pos_2, 1, p_list, content_header)
        # Accounts
        row_pos_2 += 1
        sheet_2.write(row_pos_2, 0, _('Accounts'), format_header)
        a_list = ', '.join([lt or '' for lt in filter.get('accounts')])
        sheet_2.write(row_pos_2, 1, a_list, content_header)

        # Write Ledger details
        row_pos += 3
        if filter.get('include_details', False):
            sheet.write(row_pos, 0, _('Date'),
                                    format_header)
            sheet.write(row_pos, 1, _('JRNL'),
                                    format_header)
            sheet.write(row_pos, 2, _('Account'),
                                    format_header)
            # sheet.write(row_pos, 3, _('Ref'),
            #                         format_header)
            sheet.write(row_pos, 3, _('Move'),
                                    format_header)
            sheet.write(row_pos, 4, _('Entry Label'),
                                    format_header)
            sheet.write(row_pos, 5, _('Debit'),
                                    format_header)
            sheet.write(row_pos, 6, _('Credit'),
                                    format_header)
            sheet.write(row_pos, 7, _('Balance'),
                                    format_header)
        else:
            sheet.merge_range(row_pos, 0, row_pos, 4, _('Partner'), format_header)
            sheet.write(row_pos, 5, _('Debit'),
                                    format_header)
            sheet.write(row_pos, 6, _('Credit'),
                                    format_header)
            sheet.write(row_pos, 7, _('Balance'),
                                    format_header)

        if account_lines:
            for line in account_lines:
                row_pos += 1
                sheet.merge_range(row_pos, 0, row_pos, 4, account_lines[line].get('name'), line_header)
                sheet.write(row_pos, 5, float(account_lines[line].get('debit')), line_header)
                sheet.write(row_pos, 6, float(account_lines[line].get('credit')), line_header)
                sheet.write(row_pos, 7, float(account_lines[line].get('balance')), line_header)

                if filter.get('include_details', False):

                    count, offset, sub_lines = record.build_detailed_move_lines(offset=0, partner=line,
                                                                                     fetch_range=1000000)

                    for sub_line in sub_lines:
                        _logger.info("==========================subline===========%s",sub_line.get('ldatenep'))
                        if sub_line.get('move_name') == 'Initial Balance':
                            row_pos += 1
                            sheet.write(row_pos, 4, sub_line.get('move_name'),
                                                    line_header_light_initial_bold)
                            sheet.write(row_pos, 5, float(sub_line.get('debit')),
                                                    line_header_light_initial)
                            sheet.write(row_pos, 6, float(sub_line.get('credit')),
                                                    line_header_light_initial)
                            if float(sub_line.get('balance')) > 0:
                                sheet.write(row_pos, 7,"Rs " +  str(float(sub_line.get('balance'))) + " Dr", line_header_light_initial)
                            elif float(sub_line.get('balance')) == 0:
                                sheet.write(row_pos, 7,"Rs " +  str(float(sub_line.get('balance'))) , line_header_light_initial)
                            else:
                                sheet.write(row_pos, 7,"Rs " +  str(float(abs(sub_line.get('balance')))) + " Cr", line_header_light_initial)

                        elif sub_line.get('move_name') not in ['Initial Balance','Ending Balance']:
                            row_pos += 1
                            # datestring = fields.Date.from_string(str(sub_line.get('ldatenep'))).strftime(
                            #     lang_id.date_format)
                            sheet.write(row_pos, 0, sub_line.get('ldatenep') or '',
                                                    line_header_light_date)
                            sheet.write(row_pos, 1, sub_line.get('lcode'),
                                                    line_header_light)
                            sheet.write(row_pos, 2, sub_line.get('account_name') or '',
                                                    line_header_light)
                            # sheet.write(row_pos, 3, sub_line.get('lref') or '',
                            #                         line_header_light)
                            sheet.write(row_pos, 3, sub_line.get('move_name'),
                                                    line_header_light)
                            sheet.write(row_pos, 4, sub_line.get('lname') or '',
                                                    line_header_light)
                            sheet.write(row_pos, 5,
                                                    float(sub_line.get('debit')),line_header_light)
                            sheet.write(row_pos, 6,
                                                    float(sub_line.get('credit')),line_header_light)
                            # sheet.write(row_pos, 7,
                                                    # float(sub_line.get('balance')),line_header_light)

                            if float(sub_line.get('balance')) > 0:
                                sheet.write(row_pos, 7,"Rs " +  str(float(sub_line.get('balance'))) + " Dr", line_header_light_initial)
                            elif float(sub_line.get('balance')) == 0:
                                sheet.write(row_pos, 7,"Rs " +  str(float(sub_line.get('balance'))) , line_header_light_initial)
                            else:
                                sheet.write(row_pos, 7,"Rs " +  str(float(abs(sub_line.get('balance')))) + " Cr", line_header_light_initial)

                        else: # Ending Balance
                            row_pos += 1
                            sheet.write(row_pos, 4, sub_line.get('move_name'),
                                                    line_header_light_ending_bold)
                            sheet.write(row_pos, 5, float(account_lines[line].get('debit')),
                                                    line_header_light_ending)
                            sheet.write(row_pos, 6, float(account_lines[line].get('credit')),
                                                    line_header_light_ending)
                            sheet.write(row_pos, 7, float(account_lines[line].get('balance')),
                                                    line_header_light_ending)

        # Close and return
        #################################################################
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()

    def action_view(self):
        res = {
            'type': 'ir.actions.client',
            'name': 'PL View',
            'tag': 'dynamic.pl',
            'context': {'wizard_id': self.id}
        }
        return res




class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'




    def open_partner_ledger_dynamic_view(self):

        _logger.info("=============here")
        return {
            'name': "Partner Ledger Reportt",
            'type': 'ir.actions.client',
            'tag': 'dynamic.pl.ext',
                }
