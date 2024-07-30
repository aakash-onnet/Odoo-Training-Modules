from odoo import models, api, fields


class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _inherit = ['mail.thread']
    _description = 'A model for manage Doctors of hospital.'

    name = fields.Char(string="Doctor Name", tracking=True, required=True)
    experties = fields.Char(string="Doctor Specialities", tracking=True, required=True)
    joining_date = fields.Date(string="Joining Date", tracking=True, required=True)
    experience = fields.Integer(string="Experience In Years", tracking=True, required=True)
    is_professor = fields.Boolean(string="Is Professor", tracking=True, required=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')])
    salary = fields.Float(string='Salary', tracking=True)
    active = fields.Boolean(string="Active", default=True)
