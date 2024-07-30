from odoo import models, fields, api


class Vehicle(models.Model):
    _name='vehicle'
    _description='Vehicle Model for vehicle management'
    _inherit = 'mail.thread'
    _rec_name = 'vehicle_registration_number'
    _sql_constraints = [
        ('unique_vehicle_registration_number', "UNIQUE(vehicle_registration_number)", 'Registration number must be a unique number.'),
        ('unique_chasis_number', "UNIQUE(chasis_number)", 'Chasis number must be a unique number.'),
    ]
    
    active = fields.Boolean(default=True)
    
    vehicle_registration_number = fields.Text(required=True,copy=True, tracking=True)
    
    engine_number = fields.Text(string="Engine", tracking=True)
    
    vehicle_registration_date = fields.Date(required=True, tracking=True)
    
    chasis_number = fields.Text(string="Chasis Number", copy=False, tracking=True)
    
    description = fields.Text(string="Description", tracking=True)
    
    remark = fields.Text(string="Remark", tracking=True)
    
    vehicle_creation_date = fields.Date(default=fields.Date.today(), tracking=True)

    display_name = fields.Char(string='Display Name', compute='_compute_display_name', store=True)
    
    # ! Relation Fields
    
    vehicle_account_id = fields.Many2one('account.move', string='Vehicle Account')
    
    model_id = fields.Many2one('fleet.vehicle.model', string='Vehicle Model', tracking=True)
    
    manufacturer_id = fields.Many2one('fleet.vehicle.model.brand', string='Manufacturer', tracking=True)
    
    customer_ids = fields.Many2many('res.partner', string="Customers", tracking=True)
    
    service_history_ids = fields.One2many('vehicle.service.history', 'vehicle', string='Service Histories')
    
    service_history_count = fields.Integer(compute='_compute_service_history_count')
    
    @api.depends('vehicle_registration_number')
    def _compute_display_name(self):
        for record in self:
            if record:
                print('In custom display name of fleet model')
                if record.vehicle_registration_number:
                    name = f"Vehicle - {record.vehicle_registration_number}"
                    print(type(record.display_name))
                    print(type(name))
                    record.display_name = name
    
    @api.onchange('model_id')
    def _onchange_model_id(self):
        if self.model_id:
            self.manufacturer_id = self.model_id.brand_id

    @api.depends('service_history_ids')
    def _compute_service_history_count(self):
        for record in self:
            if record.service_history_ids:
                record.service_history_count = len(record.service_history_ids)
            else:
                record.service_history_count = 0
        
    def archive_vehicle(self):
        for record in self:
            if record.active:
                record.active = False
            
    def unarchive_vehicle(self):
        for record in self:
            if not record.active:
                record.active = True