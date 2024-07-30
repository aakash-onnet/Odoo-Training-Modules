from odoo import models, fields, api
from datetime import date, timedelta
from odoo.exceptions import ValidationError

class EstatePropertyOffer(models.Model):
    _name="estate.property.offer"
    _order = "price desc"
    _description="Offer model for Property."
    
    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'Offer Price must be a positive number !')
    ]
    
    sequence = fields.Integer('Sequence' ,default=10)
    price = fields.Float(required=True)
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner')
    # ! Inverse model for one2many relationship.
    property_id = fields.Many2one('estate.property')
    description = fields.Char()
    
    create_date = fields.Datetime(string='Creation Date', readonly=True, default=lambda self: fields.Datetime.now())
    validity = fields.Integer(string='Validity (days)')
    date_deadline = fields.Date(string='Deadline Date', compute='_compute_deadline_date', inverse='_inverse_validity', store=True)

    # * Related Field
    property_type_id = fields.Many2one(
        related='property_id.property_type_id', 
        store=True,
        depends=['property_id']
    )
    
    @api.model
    def create(self, vals):
        property_obj = self.env['estate.property'].browse(vals.get('property_id'))
        
        property_obj.state = 'offer-received'
        if property_obj.best_price:
            old_offer_price = property_obj.best_price
            if vals.get('price') < old_offer_price:
                raise ValidationError(f'Offer can not be less than {old_offer_price}')
        return super().create(vals)

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.description = f"Test description from {self.partner_id.name}"
        else:
            self.description = "Dummy description."
    
    @api.depends('validity')
    def _compute_deadline_date(self):
        for record in self:
            if record.validity:
                create_date = record.create_date or fields.Datetime.now()
                record.date_deadline = create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = False

    def _inverse_validity(self):
        for record in self:
            if record.date_deadline:
                create_date = record.create_date or fields.Datetime.now()
                valid_days = record.date_deadline - create_date.date()
                record.validity = valid_days.days
            else:
                record.validity = 0
                
    @api.constrains('date_deadline')
    def _check_date_deadline(self):
        for record in self:
            if record.date_deadline and record.date_deadline <= date.today():
                raise ValidationError('Deadline date should not be a past date.')
            
    def accept_offer(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.state = 'offer-accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer = record.partner_id
            
    def reject_offer(self):
        for record in self:
            record.status = 'refused'
            if record.property_id.buyer == record.partner_id:
                record.property_id.buyer = None