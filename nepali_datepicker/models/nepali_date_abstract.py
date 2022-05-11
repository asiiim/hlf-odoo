# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import api, models
import datetime, nepali_datetime

class NepaliDate(models.AbstractModel):
    _name = 'np.date'
    _description = '''
        - Conversion to nepali date
    '''

    
    @api.model
    def get_nepalidate(self, eng_date_str, dt_format):
        """
            - Get english date string with format
            - Create datetime date object
            - Convert to nepali datetime object
            - Return nepali date string
        """
        print('English Date String >>>>>>>>>> ', eng_date_str)
        print('Date Format >>>>>>>>>> ', dt_format)
        
        dt_time = datetime.datetime.strptime(eng_date_str, dt_format)
        print('Datetime Object >>>>> ', dt_time)
        
        dt = dt_time.date()
        print('Date Object >>>>>> ', dt)
        
        ndt = nepali_datetime.date.from_datetime_date(dt)
        print('Nepali Date Object >>>>>> ', ndt)
        
        ndt_str = ndt.strftime('%Y-%m-%d')
        print('Nepali Date String >>>>>> ', ndt_str)

        return ndt_str
