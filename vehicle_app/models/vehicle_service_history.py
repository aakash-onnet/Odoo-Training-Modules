from odoo import models, fields, api
from datetime import timedelta


class VehicleServiceHistory(models.Model):
    _name='vehicle.service.history'
    _description='For keep record of service history'
    _sql_constraints = [
        ('account_move_id_unique', 'unique(account_move_id)', 'Each account move can only have one service history!')
    ]
    

    date = fields.Date(string="Date")
    
    vehicle_registration_number = fields.Text(string="Vehicle Registration Number", readonly=True, store=True, related='vehicle.vehicle_registration_number')
    
    vehicle_remarks = fields.Text(string="Vehicle Remarks", readonly=True, store=True, related='vehicle.remark')
    
    usage_mileage = fields.Float(string="Usage/Mileage (KM)", related='account_move_id.usage_mileage') # X
    
    invoice_number = fields.Char(string="Invoice Number / Sales Return Number")
    
    item_code = fields.Char(string="Item Code")
    
    item_name = fields.Char(string="Item Name")
    
    item_remarks = fields.Char(string="Item Remarks")
    
    remarks = fields.Text(string="Remarks")
    
    quantity = fields.Float(string="Quantity")
    
    price = fields.Float(string="Price")
    
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True)
    
    invoice_amount = fields.Monetary(string="Invoice Amount", curreny_field='currency_id')
    
    cost = fields.Float(string="Cost")

    # ! Relation Fields
    
    vehicle = fields.Many2one('vehicle', string='Vehicle', domain="[('vehicle_account_id', '!=', None)]")
    
    branch = fields.Many2one('res.company', string="Branch")
    
    customer_name = fields.Many2one('res.partner', string="Customer Name")
    
    vehicle_model = fields.Many2one('fleet.vehicle.model', string="Vehicle Model", readonly=True, store=True, related='vehicle.model_id')
    
    uom = fields.Many2one('uom.uom', string="UoM")
    
    salesman = fields.Many2one('res.users', string="Salesman / Technician")
    
    supplier = fields.Many2one('res.partner', string="Supplier")

    account_move_id = fields.Many2one('account.move', string='Account Move', readonly=True)
    
    account_move_line_id = fields.Many2one('account.move.line', string="Account Move Line", domain="[('move_id.vehicle', '=', vehicle)]")
                                                         
    @api.onchange('account_move_line_id')
    def _onchange_account_move_line_id(self):
        if self.account_move_line_id:
            self.account_move_id = self.account_move_line_id.move_id
            print('Account Move ID : ', self.account_move_id)
            self.usage_mileage = self.account_move_id.usage_mileage
            self.remarks = self.account_move_id.remarks
            self.date = self.account_move_id.invoice_date
            self.invoice_number = self.account_move_id.name
            self.item_code = self.account_move_line_id.product_id.default_code
            self.item_name = self.account_move_line_id.product_id.name
            self.item_remarks = self.account_move_line_id.product_id.description_purchase
            self.remarks = self.account_move_id.remarks
            self.quantity = self.account_move_line_id.quantity
            self.price = self.account_move_line_id.price_unit
            self.invoice_amount = self.account_move_id.amount_total
            self.cost = self.account_move_line_id.cost
            self.branch = self.account_move_id.company_id
            self.customer_name = self.account_move_id.partner_id
            self.uom = self.account_move_line_id.product_uom_id
            self.salesman = self.account_move_id.user_id
            self.supplier = self.account_move_line_id.supplier
            self.currency_id = self.account_move_id.currency_id 
