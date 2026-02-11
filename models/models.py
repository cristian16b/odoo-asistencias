# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class asistencia_por_departamento(models.Model):
#     _name = 'asistencia_por_departamento.asistencia_por_departamento'
#     _description = 'asistencia_por_departamento.asistencia_por_departamento'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

