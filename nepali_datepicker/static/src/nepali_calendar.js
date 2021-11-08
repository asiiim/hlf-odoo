// Part of 10 Orbits Pvt. Ltd. See LICENSE for full copyright and licensing details.
odoo.define('nepali_datepicker.form_widgets', function (require) {
	"use strict";

	var basicFields = require('web.basic_fields');

	var FieldDate = basicFields.FieldDate.include({
		/**
		* In readonly mode, the date field is displayed along with nepali date, formatted as:
		*	date_ad (date_bs)
		*
		* @override
		*/
		_renderReadonly: function () {
			this._super();
			if (this.field.type == 'date' && this.$el.text()) {
				var adDate = this.value;
				var bsDate = calendarFunctions.getBsDateByAdDate(adDate.year(), adDate.month()+1, adDate.date());
				var bsDateInFormat = calendarFunctions.bsDateFormat("%y-%m-%d", bsDate['bsYear'], bsDate['bsMonth'], bsDate['bsDate']);
				this.$el.text(this.$el.text().concat(" (", bsDateInFormat, ")"));
			}
		},
	});
});
