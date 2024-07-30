from odoo import _, models, fields, api
from datetime import date, timedelta
from odoo.exceptions import UserError, ValidationError # type: ignore
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _inherit = ['mail.thread']
    _order = "id desc"
    _description = "Model to manage data of property in real estate business."
    
    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'Property Name must be unique !'),
        ('check_expected_price', 'CHECK(expected_price>0)', 'Price can not be Negative Value !'),
        ('check_selling_price', 'CHECK(selling_price>0)', 'Selling Price can not be Negative Value !'),
        ('check_best_price', 'CHECK(best_price>0)', 'Offer Price can not be Negative Value !'),
    ]    
    
    name = fields.Char(string="Property Name", required=True, default='Unknown', tracking=True)
    last_seen = fields.Datetime("Last Seen" , default=fields.Datetime.now, tracking=True)
    description = fields.Text(string="Property Description", tracking=True)
    postcode = fields.Char(string="Post Code", tracking=True)
    date_availability = fields.Date(copy=False, default=lambda self:date.today() + timedelta(days=90), tracking=True)
    expected_price = fields.Float(required=True, tracking=True)
    selling_price = fields.Float(readonly=True, copy=False, tracking=True)
    bedrooms = fields.Integer(default=2, tracking=True)
    living_area = fields.Integer(tracking=True)
    facades = fields.Integer(tracking=True)
    garage = fields.Boolean(tracking=True)
    garden = fields.Boolean(tracking=True)
    garden_area = fields.Integer(tracking=True)
    
    garden_orientation = fields.Selection([
        ('north', 'North'), 
        ('south', 'South'),
        ('east', 'East'), 
        ('west', 'West')
        ], tracking=True)
    
    state = fields.Selection([
        ('new', 'New'),
        ('offer-received', 'Offer Received'),
        ('offer-accepted', 'Offer Accepted'),
        ('sold','Sold'),
        ('cancelled', 'Cancelled')
        ], 
        copy=False, 
        default='new', 
        tracking=True)
    
    active = fields.Boolean(default=True, tracking=True)
    
    # * Relationship Fields
    buyer = fields.Many2one("res.partner", string="Buyer", readonly=True)
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    salesperson = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True, default=lambda self: self.env.user)

    tag_ids = fields.Many2many('estate.property.tag', string="Property Tags")
    # * To define one2many relationship we have to define many2one relation in corresponding field also.
    # ! To display more than one records we also use one2many relationship. one -> property <-> many -> offers
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offer2")
    
    # * Computed Fields
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_offer_price")
    

    # ! Normal Way to override unlink method    
    # def unlink(self):
    #     for record in self:
    #         if record.state not in ['new', 'cancelled']:
    #             raise UserError('You can only delete New and Cancelled properties.')
    #     return super().unlink()
    
    # * Optimised way to override delete method
    @api.ondelete(at_uninstall=False)
    def _check_state_before_delete(self):
        for record in self:
            if record.state not in ['new', 'canceled']:
                raise UserError('You cannot delete a property if its state is not New or Canceled.')
        
    
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area
            
    @api.depends('offer_ids')
    def _compute_best_offer_price(self):
        for record in self:
            if len(record.offer_ids) > 0:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0
                
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_orientation = 'north'
            self.garden_area = 10
        else:
            self.garden_orientation = ''
            self.garden_area = 0
            
    @api.onchange("garden_area")
    def _onchange_garden_area(self):
        if self.garden_area and self.garden_area < 10:
            return {'warning': {
                'title': _("Warning"),
                'message': ('Garden can not be this small.')}}
            
    def sold_property(self):
        """Sold property and set state according to that."""
        for record in self:
            if record.state == 'cancelled':
                raise UserError("You can not sold cancelled property.")
            else:
                record.state = 'sold'

    def cancel_property(self):
        """Cancel property and set state as cancelled."""
        for record in self:
            if record.state == 'sold':
                raise UserError("You can not cancel sold property.")
            else:
                record.state = 'cancelled'
                
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        """Checking that selling price should not be lesser than 90% of expected price."""
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):  # Specify precision_digits
                negotiable_price = (record.expected_price * 0.9)
                if float_compare(record.selling_price, negotiable_price, precision_digits=2) < 0:  # Specify precision_digits
                    raise ValidationError("Selling price cannot be lower than 90% of the expected price. You must reduce the expected price to accept this offer !!!")