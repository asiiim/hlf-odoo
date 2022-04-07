# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import api, models
from odoo.exceptions import UserError
from odoo.addons import decimal_precision as dp
from num2words import num2words

import logging
_logger = logging.getLogger(__name__)


class CustomAbstract(models.AbstractModel):
    _name = 'custom.abstract'
    _description = '''
        This abstract model consists of general methods
        need for the custom reports.
    '''

    
    @api.model
    def get_amount_to_words(self, amount):
        """
            Need to call the num2words method twice because
            by default the digit after point is pronounced
            as Example: ".88" = eight eight, but expected eighty eight 
        """
        amount_split_list = str(amount).split(".")
        rupees_digit = int(amount_split_list[0])
        paisa_digit = int(amount_split_list[1])
        rupees = num2words(rupees_digit, lang='en_IN')
        paisa = num2words(paisa_digit, lang='en_IN')
        amount_words = rupees.capitalize() + ' rupees and ' \
            + paisa + ' paisa.'
        amount_words = amount_words.replace(",", "")
        return amount_words


    @api.model
    def display_partner_details(self, partner_id):
        """
            This method simply returns qweb displayable partner details.
        """
        partner_address = []
        partner_address.append(partner_id.name)
        if partner_id.street:
            partner_address.append(partner_id.street)
        
        street_city_zip = ""
        if partner_id.street2:
            street_city_zip += partner_id.street2
            street_city_zip += ", "
        if partner_id.city:
            street_city_zip += partner_id.city
            street_city_zip += ", "
        if partner_id.zip:
            street_city_zip += partner_id.zip
        if street_city_zip:
            partner_address.append(street_city_zip)

        state_country = ""
        if partner_id.state_id:
            state_country += partner_id.state_id.name
            state_country += ", "
        if partner_id.country_id:
            state_country += partner_id.country_id.name
        if state_country:
            partner_address.append(state_country)

        print(partner_address)
        return partner_address
        
        
        
