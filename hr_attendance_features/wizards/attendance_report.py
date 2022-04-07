import datetime
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import dateutil.parser

class AttendanceReport(models.TransientModel):
    _name = 'attendance.monthly.report'
    _description = 'Monthly Attendance Report'

    start_date = fields.Date('From', required=True)
    end_date = fields.Date('To', required=True, default=datetime.date.today())
    employees_id = fields.Many2many(comodel_name='hr.employee', string = 'Employees')
    total_days = fields.Integer('Total Days', compute="_get_days", readonly=1)
    weekly_off_days = fields.Integer('Weekly Off', compute="_get_days", readonly=1)
    holidays = fields.Integer('Holidays', compute="_get_days", readonly=1)
    

    # This method is used for looping through each between two dates
    def _date_range(self):
        for n in range(int((self.end_date - self.start_date).days)):
            yield self.start_date + datetime.timedelta(n)

    # Count no. of days list of datetimes
    def _days_between_datetimes(self, datetimes):
        date_count = []
            
        for dt in datetimes:
            dateonly = dt.date()
            date_count.append(dateonly)
        
        date_count = len(set(date_count))
        
        return date_count
    
    
    @api.onchange('start_date', 'end_date')
    def _get_days(self):

        for rec in self:
            if rec.start_date and rec.end_date:

                # total days
                date_diff = rec.end_date - rec.start_date
                rec.total_days = int(date_diff.days)

                # count weekly off between two dates
                weekly_off_count = 0
                for dt in self._date_range():
                    if dt.isoweekday() == 6:
                        # isoweekday = 6 means Saturday
                        weekly_off_count += 1
                rec.weekly_off_days = weekly_off_count

                # holidays
                holidays = self.env['resource.calendar.leaves'].search([
                    ('date_from', '>=', self.start_date), 
                    ('date_from', '<=', self.end_date)
                ])
                holiday_count = 0
                for hday in holidays:
                    holiday_count += (hday.date_to - hday.date_from).days
                rec.holidays = holiday_count



    def hr_attendance_monthly_report(self):

        # Get the available attendances in the selected date range
        attendances = self.env['hr.attendance'].search([
            ('check_in', '>=', self.start_date), ('check_in', '<=', self.end_date)])

        
        # This contains the actual data that we are intending to print in
        # pdf report.
        report_data = []

        
        # Check if we need to select all employees or selected employees.
        if not self.employees_id:
            employees = self.env['hr.employee'].search([])
        else:
            employees = self.employees_id

        for emp in employees:
            
            # Get attendances records of the selected employee
            emp_attnd = attendances.filtered(lambda x: x.employee_id.id == emp.id)
            emp_attnd_dates = emp_attnd.mapped('check_in')

            # count present days
            # present_dates = []
            
            # for dt in emp_attnd_dates:
            #     empdate = dt.date()
            #     present_dates.append(empdate)
            
            # present_days = len(set(present_dates))
            present_days = self._days_between_datetimes(emp_attnd_dates)

            report_data.append({
                'id': emp.id,
                'name': emp.name,
                'supervisor': emp.first_supervisor.name,
                'company': emp.company_id.name,
                'hq': emp.user_id.partner_id.team_id.name,
                'present': present_days,
                'absent': self.total_days - present_days - self.weekly_off_days \
                    - self.holidays
            })

        data = {
            'form': self.read()[0],
            'report_data': report_data,
        }

        return self.env.ref('hr_attendance_features.action_hr_attendance_monthly_report').report_action(self, data=data)
