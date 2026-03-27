# Copyright 2024 Manuel Calero (https://xtendoo.es)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models, fields


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    product_line_name = fields.Char(
        compute='_compute_product_text',
        store=True,
    )

    @api.depends('product_id')
    def _compute_product_text(self):
        for record in self.filtered('name'):
            record.product_line_name = record.name.split(']', 1)[-1].split('\n', 1)[0] if ']' in record.name else record.name
