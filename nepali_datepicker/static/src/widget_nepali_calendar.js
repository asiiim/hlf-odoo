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
			if (adDate) {
				var bsDate = calendarFunctions.getBsDateByAdDate(adDate.year(), adDate.month()+1, adDate.date());
				var bsDateInFormat = calendarFunctions.bsDateFormat("%y-%m-%d", bsDate['bsYear'], bsDate['bsMonth'], bsDate['bsDate']);

				return bsDateInFormat;
			}
		},


		/**
		* set date in BS
		*/
		set_value_bs: function() {
			var adDate = this.getValue();
			// if ((this.getParent().format == 'L') || (this.getParent().field.type == 'date')) {
			// 	if (!this.datewidgetBs) {
			// 		this.build_widget_bs();
			// 	}
			// 	this.dateValueBs = this.get_value_bs(adDate);
			// 	this.datewidgetBs.val(this.dateValueBs);
			// }

			if (!this.datewidgetBs) {
				this.build_widget_bs();
			}
			this.dateValueBs = this.get_value_bs(adDate);
			this.datewidgetBs.val(this.dateValueBs);
		},


		/**
		* set date in BS
		*
    * @override
    */
		changeDatetime: function(e) {
		  if (this.__libInput > 0) {
            if (this.options.warn_future) {
                this._warnFuture(this.getValue());
            }
            this.trigger("datetime_changed");
            this.set_value_bs();
            return;
        }
        var oldValue = this.getValue();
        if (this.isValid()) {
            this._setValueFromUi();
            var newValue = this.getValue();
            var hasChanged = !oldValue !== !newValue;
            if (oldValue && newValue) {
                var formattedOldValue = oldValue.format(time.getLangDatetimeFormat());
                var formattedNewValue = newValue.format(time.getLangDatetimeFormat());
                if (formattedNewValue !== formattedOldValue) {
                    hasChanged = true;
                }
            }
            if (hasChanged) {
                if (this.options.warn_future) {
                    this._warnFuture(newValue);
                }
                this.trigger("datetime_changed");
                this.set_value_bs();
            }
        } else {
            var formattedValue = oldValue ? this._formatClient(oldValue) : null;
            this.$input.val(formattedValue);
        }
    },


		/**
     	* @override
     	*/
		_onDateTimePickerShow: function () {
			this._super();
			if ((this.getParent().format == 'L') || (this.getParent().field.type==='date' && this.datewidgetBs.showFlag)) {
				this.__libInput++;
				this.$el.datetimepicker('hide');
				this.__libInput--;
				this.datewidgetBs.showFlag = false;
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

			this.datewidgetBs.on("show",  function (event) {
				self.datewidgetBs.showFlag = true;
			});

			this.datewidgetBs.on("dateChange dateSelect", function (event) {
				var adDate = moment(event.datePickerData.adDate).format(self.options.format);
				self.setValue(self._parseClient(adDate));
				self.trigger('datetime_changed');
				self.datewidgetBs.showFlag = false;
				});

			this.datewidgetBs.appendTo(this.$el);
		},


		/**
		* build Nepali datepicker if it does not exist
		*
     	* @override
     	*/
		start: function () {
	        this.$input = this.$('input.o_datepicker_input');
	        this.__libInput++;
	        this.$el.datetimepicker(this.options);
	        this.__libInput--;
	        this._setReadonly(false);

			// if ((this.getParent().format == 'L') || (this.getParent().field.type === 'date' && !this.datewidgetBs)) {
			// 	this.build_widget_bs();
			// }

			this.build_widget_bs();
		},

	});
});
