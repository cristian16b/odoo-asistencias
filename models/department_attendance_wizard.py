from odoo import models, fields, api
from datetime import datetime, timedelta


class DepartmentAttendanceWizard(models.Model):
    _name = 'department.attendance.wizard'
    _description = 'Wizard para registrar asistencias por departamento'

    department_id = fields.Many2one(
        'hr.department',
        string="Departamento",
        required=True
    )

    start_date = fields.Date(
        string="Fecha",
        required=True
    )

    start_time = fields.Float(
        string="Hora inicio",
        required=True
    )

    employee_line_ids = fields.One2many(
        'department.attendance.line',
        'wizard_id',
        string="Empleados"
    )

    # 🔹 BOTÓN PARA CARGAR EMPLEADOS
    def action_load_employees(self):
        self.ensure_one()

        if not self.department_id:
            return

        employees = self.env['hr.employee'].search([
            ('department_id', '=', self.department_id.id)
        ])

        self.employee_line_ids = [(5, 0, 0)]

        base_dt = datetime.combine(
            self.start_date,
            datetime.min.time()
        ) + timedelta(hours=self.start_time)

        lines = []
        for emp in employees:
            lines.append((0, 0, {
                'employee_id': emp.id,
                'check_in': base_dt,
                'hours_worked': 0.0,
            }))

        self.employee_line_ids = lines

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'department.attendance.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'current',
        }


    # 🔹 CONFIRMAR ASISTENCIAS
    def action_confirm(self):
        self.ensure_one()

        for line in self.employee_line_ids:

            if not line.employee_id:
                continue  # seguridad extra

            if line.check_in:
                check_out_dt = line.check_in + timedelta(hours=line.hours_worked)
            else:
                check_out_dt = False

            self.env['hr.attendance'].create({
                'employee_id': line.employee_id.id,
                'check_in': line.check_in,
                'check_out': check_out_dt,
            })
