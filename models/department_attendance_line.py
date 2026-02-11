from odoo import models, fields, api
from datetime import datetime, timedelta

class DepartmentAttendanceLine(models.TransientModel):
    _name = 'department.attendance.line'
    _description = 'Líneas de empleados en el wizard de asistencia'

    wizard_id = fields.Many2one(
        'department.attendance.wizard',
        string="Wizard",
        required=True,
        ondelete='cascade'
    )
    employee_id = fields.Many2one('hr.employee', string="Empleado", required=True)
    check_in = fields.Datetime(string="Entrada")
    hours_worked = fields.Float(string="Horas trabajadas")
    check_out = fields.Datetime(string="Salida", compute="_compute_check_out")

    @api.depends('check_in', 'hours_worked')
    def _compute_check_out(self):
        for line in self:
            if line.check_in and line.hours_worked:
                line.check_out = line.check_in + timedelta(hours=line.hours_worked)
            else:
                line.check_out = False
