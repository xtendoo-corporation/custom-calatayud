# Copyright 2023 Jaime Millan (https://xtendoo.es)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models, fields


class ProductProduct(models.Model):
    _inherit = 'product.product'

    wholesale_price = fields.Float(
        string='Tarifa mayorista',
        compute='_compute_wholesale_price',
    )

    def _compute_wholesale_price(self):
        self.wholesale_price = 0.0
        pricelist = self.env['product.pricelist'].search([('name', '=', 'Tarifa mayorista')])
        if not pricelist:
            return
        pricelist_item = pricelist.item_ids[0]
        if not pricelist_item:
            return
        order_date = fields.Date.today()
        qty = 1.0
        for product in self:
            product.wholesale_price = pricelist_item._compute_price(product, qty, product.uom_id, order_date)
