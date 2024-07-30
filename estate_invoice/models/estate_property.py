from odoo import models, fields, Command


class EstatePropertyAccount(models.Model):    
    _inherit = 'estate.property'
    
    def sold_property(self):
        # Ensure that the property is sold before creating an invoice
        parent_call = super().sold_property()
        
        print("Invoice Module Start.", self.state)

        if self.state != 'sold':
            return

        # Create an empty account.move (invoice)
        invoice_vals = {
            'partner_id': self.buyer.id,
            'move_type': 'out_invoice',  # 'out_invoice' corresponds to Customer Invoice
            'invoice_line_ids': [
                (0, 0, {
                    'name': 'Commission Fee',
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06
                }),
                (0, 0, {
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': 100.00
                })
            ]
        }
        print(invoice_vals)

        # Create the invoice
        self.env['account.move'].create(invoice_vals)
        
        return parent_call