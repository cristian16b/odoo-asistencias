from odoo import models, fields, api
from datetime import datetime, timedelta

class DepartmentAttendanceWizard(models.TransientModel):
    _name = 'department.attendance.wizard'
    _description = 'Wizard para registrar asistencias por departamento'

    department_id = fields.Many2one('hr.department', string="Departamento")
    start_date = fields.Date(string="Fecha")
    start_time = fields.Float(string="Hora inicio")
    employee_line_ids = fields.One2many(
        'department.attendance.line',
        'wizard_id',
        string="Empleados"
    )
    

    @api.onchange('department_id')
    def _onchange_department_id(self):
        if self.department_id:
            employees = self.env['hr.employee'].search([
                ('department_id', '=', self.department_id.id)
            ])
            # Generar check_in base con fecha + hora inicio
            if self.start_date and self.start_time is not None:
                base_dt = datetime.combine(self.start_date, datetime.min.time()) + timedelta(hours=self.start_time)
            else:
                base_dt = False

            self.employee_line_ids = [(0, 0, {
                'employee_id': emp.id,
                'check_in': base_dt,
                'hours_worked': 0,
            }) for emp in employees]

    def action_confirm(self):
        for line in self.employee_line_ids:
            if line.check_in and line.hours_worked:
                check_out_dt = line.check_in + timedelta(hours=line.hours_worked)
            else:
                check_out_dt = False

            self.env['hr.attendance'].create({
                'employee_id': line.employee_id.id,
                'check_in': line.check_in,
                'check_out': check_out_dt,
            })


# from odoo import models, fields, api
# from datetime import datetime, timedelta

# class DepartmentAttendanceWizard(models.TransientModel):
#     _name = 'department.attendance.wizard'
#     _description = 'Wizard para registrar asistencias por departamento'

#     department_id = fields.Many2one('hr.department', string='Departamento', required=True)
#     start_date = fields.Date(string='Fecha de inicio', required=True)
#     start_time = fields.Float(string='Hora de inicio', required=True,
#                               help="Hora en formato decimal, ej: 8.5 = 8:30")

#     employee_line_ids = fields.One2many(
#         'department.attendance.line',
#         'wizard_id',
#         string='Empleados'
#     )

#     @api.onchange('department_id')
#     def _onchange_department_id(self):
#         if self.department_id:
#             employees = self.department_id.employee_ids
#             lines = []
#             for emp in employees:
#                 lines.append((0, 0, {
#                     'employee_id': emp.id,
#                 }))
#             self.employee_line_ids = lines

#     def action_confirm(self):
#         for line in self.employee_line_ids:
#             if line.hours_worked:
#                 # Construir datetime de entrada
#                 start_dt = datetime.combine(self.start_date, datetime.min.time())
#                 start_dt = start_dt + timedelta(hours=self.start_time)

#                 # Calcular salida
#                 end_dt = start_dt + timedelta(hours=line.hours_worked)

#                 # Crear registro en hr.attendance
#                 self.env['hr.attendance'].create({
#                     'employee_id': line.employee_id.id,
#                     'check_in': start_dt,
#                     'check_out': end_dt,
#                 })


# class DepartmentAttendanceLine(models.TransientModel):
#     _name = 'department.attendance.line'
#     _description = 'Línea de empleados para asistencia'

#     wizard_id = fields.Many2one('department.attendance.wizard', string='Wizard')
#     employee_id = fields.Many2one('hr.employee', string='Empleado', required=True)
#     hours_worked = fields.Float(string='Horas trabajadas')
#     check_in = fields.Datetime(string='Entrada', compute='_compute_times', store=True)
#     check_out = fields.Datetime(string='Salida', compute='_compute_times', store=True)

#     @api.depends('hours_worked', 'wizard_id.start_date', 'wizard_id.start_time')
#     def _compute_times(self):
#         for line in self:
#             if line.wizard_id.start_date and line.wizard_id.start_time:
#                 start_dt = datetime.combine(line.wizard_id.start_date, datetime.min.time())
#                 start_dt = start_dt + timedelta(hours=line.wizard_id.start_time)
#                 line.check_in = start_dt
#                 if line.hours_worked:
#                     line.check_out = start_dt + timedelta(hours=line.hours_worked)
#                 else:
#                     line.check_out = False
