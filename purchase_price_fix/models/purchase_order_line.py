from odoo import models, api

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.depends('product_id', 'order_id.partner_id')
    def _compute_price_unit_and_date_planned_and_name(self):
        super()._compute_price_unit_and_date_planned_and_name()

        for line in self.filter(lambda l: l.product_id and not l.display_type, self):
            if not line.price_unit or line.price_unit == 0:
                line.price_unit = line.product_id.standard_price
