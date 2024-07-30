from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'


    vehicle = fields.Many2one('vehicle', string='Vehicle')

    vehicle_registration_number = fields.Text(string="Vehicle Registration Number", readonly=True, related="vehicle.vehicle_registration_number")
    
    vehicle_remarks = fields.Text(string="Vehicle Remarks", readonly=True, related="vehicle.remark")
    
    usage_mileage = fields.Float(string="Usage/Mileage (KM)")
    
    remarks = fields.Text(string="Remarks")

    @api.model
    def create(self, vals):
        account_obj = super().create(vals)
        if vals.get('vehicle'):
            vehicle_obj = self.env['vehicle'].browse(vals.get('vehicle'))
            vehicle_obj.vehicle_account_id = account_obj.id
        return account_obj