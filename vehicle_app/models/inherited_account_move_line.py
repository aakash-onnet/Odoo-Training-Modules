from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    cost = fields.Float(string="Cost")
    supplier = fields.Many2one('res.partner', string="Supplier")

    @api.depends('quantity', 'discount', 'price_unit', 'tax_ids', 'currency_id', 'cost')
    def _compute_totals(self):
        for line in self:
            if line.display_type != 'product':
                line.price_total = line.price_subtotal = False
                continue

            # Compute 'price_subtotal' with cost.
            line_discount_price_unit = (line.price_unit * (1 - (line.discount / 100.0))) + line.cost
            subtotal = (line.quantity * line_discount_price_unit)
            print('Unit Price with cost : ', line_discount_price_unit)
            print(subtotal)

            # Compute 'price_total' with tax.
            if line.tax_ids:
                taxes_res = line.tax_ids.compute_all(
                    line_discount_price_unit,
                    quantity=line.quantity,
                    currency=line.currency_id,
                    product=line.product_id,
                    partner=line.partner_id,
                    is_refund=line.is_refund,
                )
                line.price_subtotal = taxes_res['total_excluded']
                print('Tax Excluded : ', taxes_res['total_excluded'])
                line.price_total = taxes_res['total_included']
                print('Tax Included : ', taxes_res['total_included'])
            else:
                line.price_total = line.price_subtotal = subtotal

    @api.onchange('cost', 'quantity', 'discount', 'price_unit', 'tax_ids', 'currency_id')
    def _onchange_totals(self):
        self._compute_totals()
        if self.move_id:
            self.move_id._compute_amount()