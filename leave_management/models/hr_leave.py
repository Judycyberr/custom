# -*- coding: utf-8 -*-
from odoo import fields,models,api
from odoo.exceptions import ValidationError


class HrLeave(models.Model):
    _inherit = "hr.leave"

    emp_name_leave = fields.Char(string="Employee Name")

    def action_approve(self, check_state=True):
        print("working")
        print("dept",self.department_id)
        print("employee",self.employee_id.name)
        # emp = self.env['hr.employee'].search_count([('department_id', '=', self.department_id)])
        # print("All emp under dept :",emp)
        # leave_emp = self.env['hr.employee'].search_count([('active', '=', False),('department_id', '=', self.department_id)])
        leave_e = self.env['hr.employee'].search([('department_id', '=', self.department_id)])
        # for rec in leave_e:
        #     self.emp_name_leave = self.emp_name_leave + rec.name
        # print("All leaves :",leave_emp)
        # if leave_emp >= emp/2:
        #     raise ValidationError("50% of the employee are leaves"+self.emp_name_leave)
        #
        leaves = self.env['hr.leave'].search([('employee_id', '=', self.employee_id)])
        print("leaves",leaves)
        for rec in leaves:
            print("from_date",rec.date_from)
            print("to_date",rec.date_to)
        other_leaves = self.env['hr.leave'].search([('employee_id', '=', leave_e)])
        print("other_leaves",other_leaves)
        print("all employ in department",leave_e)
        for rec in other_leaves:
            print(rec.employee_id.name)
            print("from_date",rec.date_from)
            print("to_date", rec.date_to)
        res = super().action_approve(check_state)
        return res
