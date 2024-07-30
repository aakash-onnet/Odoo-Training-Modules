from odoo import models, fields, api


class EstatePropertyTag(models.Model):
    _name="estate.property.tag"
    _order = "name desc"
    _description="Tag model to add tags in property."
    
    name = fields.Char(required=True, string="Property Tag") 
    sequence = fields.Integer('Sequence', default=12)
    Color = fields.Integer()
    
    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'Property Tag must be unique !'),
    ]