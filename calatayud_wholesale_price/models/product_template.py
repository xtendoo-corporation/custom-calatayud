# Copyright 2023 Jaime Millan (https://xtendoo.es)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    wholesale_price = fields.Float(
        string='Tarifa mayorista',
        compute='_compute_wholesale_price',
    )

    def _compute_wholesale_price(self):
        self.wholesale_price = 0.0
        pricelist_id = self.env['product.pricelist'].search([('name', '=', 'Tarifa mayorista')], limit=1)
        if not pricelist_id:
            return
        for product_id in self:
            wholesale_price = pricelist_id._get_product_price(
                product_id, 1.0, uom=product_id.uom_id, date=fields.Date.today(),
            )
            product_id.wholesale_price = wholesale_price
