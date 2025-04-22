from odoo import api, models

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.onchange('product_id', 'partner_id', 'product_qty', 'date_planned')
    def _onchange_product_price_fallback(self):
        for line in self:
            # Validar que hay producto seleccionado
            if not line.product_id:
                continue

            # Si ya tiene precio (> 0), respetamos ese valor
            if line.price_unit and line.price_unit > 0:
                continue

            # Solo aquí llamamos a _select_seller si hay un único product_id
            supplier = line.product_id._select_seller(
                partner_id=line.partner_id,
                quantity=line.product_qty,
                date=line.date_planned and line.date_planned.date()
            )

            if not supplier or supplier.price == 0.0:
                line.price_unit = line.product_id.standard_price
