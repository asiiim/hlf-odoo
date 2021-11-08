// Part of 10 Orbits Pvt. Ltd. See LICENSE for full copyright and licensing details.
odoo.define('nepali_datepicker.date_widget', function (require) {
	"use strict";

	var Widget = require('web.datepicker');
	var time = require('web.time');

	Widget.DateWidget.include({
		/**
		* get date in BS (YYYY-MM-DD)
		*/
		get_value_bs: function(adDate) {
			var bsDate = calendarFunctions.getBsDateByAdDate(adDate.year(), adDate.month()+1, adDate.date());
			var bsDateInFormat = calendarFunctions.bsDateFormat("%y-%m-%d", bsDate['bsYear'], bsDate['bsMonth'], bsDate['bsDate']);

			return bsDateInFormat;
		},


		/**
		* set date in BS
		*/
		set_value_bs: function() {
			if (this.getParent().field.type == 'date') {
				var adDate = this.getValue();
				if (!this.datewidgetBs) {
					this.build_widget_bs();
				}
				this.dateValueBs = this.get_value_bs(adDate);
				this.datewidgetBs.val(this.dateValueBs);
			}
		},


		/**
		* set date in BS
		*
     	* @override
     	*/
		changeDatetime: function(e) {
	        if (this.isValid()) {
	            var oldValue = this.getValue();
	            this._setValueFromUi();
	            var newValue = this.getValue();
	            var hasChanged = !oldValue !== !newValue;
	            if (oldValue && newValue) {
	                var formattedOldValue = oldValue.format(time.getLangDatetimeFormat());
	                var formattedNewValue = newValue.format(time.getLangDatetimeFormat())
	                if (formattedNewValue !== formattedOldValue) {
	                    hasChanged = true;
	                }
	            }

	            if (hasChanged) {
	                // The condition is strangely written; this is because the
	                // values can be false/undefined
	                this.trigger("datetime_changed");
					this.set_value_bs();
	            }
	        }
		},


		/**
		* Build Nepali datepicker input field and handle events
		*/
		build_widget_bs: function() {
			this.datewidgetBs = $("<input/>", {
				"type": "text",
				"id": "datepicker_nepali_bs2",
			});

			this.dateValueBs = '';

			this.datewidgetBs.nepaliDatePicker({
				dateFormat: '%y-%m-%d',
				closeOnDateSelect: true
			});

			var self = this;
			this.datewidgetBs.on("dateChange dateSelect", function (event) {
				var adDate = moment(event.datePickerData.adDate).format(self.options.format);
				self.setValue(self._parseClient(adDate));
				self.trigger('datetime_changed');
				});

			this.datewidgetBs.appendTo(this.$el);
		},


		/**
		* build Nepali datepicker if it does not exist
		*
     	* @override
     	*/
		start: function() {
			this.$input = this.$('input.o_datepicker_input');
        	this.$el.datetimepicker(this.options);
        	this.picker = this.$el.data('DateTimePicker');
        	this._setReadonly(false);

			if ((this.getParent().format == 'L') || (this.getParent().field.type === 'date' && !this.datewidgetBs)) {
				this.build_widget_bs();
			}
		},
	});
});
