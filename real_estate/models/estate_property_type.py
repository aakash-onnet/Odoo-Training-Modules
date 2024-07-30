from odoo import models,fields,api # type: ignore


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _order = "name desc"
    _description = 'A model for type of property.'
    
    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'Property Type must be unique!'),
    ]
    
    name = fields.Char(required=True,string='Property Type')  
    sequence = fields.Integer('Sequence', default=10, help="Used to order stages. Lower is better.")
    property_ids = fields.One2many('estate.property', 'property_type_id', string="X")
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute="_compute_offer_count")
    
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            if record.offer_ids:
                record.offer_count = len(record.offer_ids)
            else:
                record.offer_count = 0    