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
        pricelist = self.env['product.pricelist'].search([('name', '=', 'Tarifa mayorista')])
        if not pricelist:
            return
        pricelist_item = pricelist.item_ids[0]
        if not pricelist_item:
            return
        for product in self:
            order_date = fields.Date.today()
            qty = 1.0
            uom = product.uom_id
            product.wholesale_price = pricelist_item._compute_price(product, qty, uom, order_date)

