from odoo import models, fields, api


class HosiptalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread']
    _description = "A model to manage patient of hospital."

    name = fields.Char(string="Patient Name", required=True, tracking=True)
    dob = fields.Date(string="DOB", tracking=True)
    gender = fields.Selection([("male", "Male"), ("female", "Female")], string="Gender", tracking=True)
