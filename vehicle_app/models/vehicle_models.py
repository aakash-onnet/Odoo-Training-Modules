from odoo import models,fields, api


class VehicleModels(models.Model):
    _inherit = 'fleet.vehicle.model'
        
    @api.depends('brand_id')
    def _compute_display_name(self):
        for record in self:
            print('In custom display name of fleet model')
            name = record.name
            if record.brand_id.name:
                name = f"{record.brand_id.name}({name})"
            record.display_name = name
