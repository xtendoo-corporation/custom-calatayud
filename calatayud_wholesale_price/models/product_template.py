# Copyright 2023 Jaime Millan (https://xtendoo.es)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    wholesale_price = fields.Float(
        string='Tarifa mayorista',
        compute='_compute_wholesale_price',
        store=True,
    )

    pricelist_item_ids = fields.One2many(
        comodel_name='product.pricelist.item',
        inverse_name='product_id',
        string='Pricelist Items',
    )

    @api.depends('list_price', 'pricelist_item_ids')
    def _compute_wholesale_price(self):
        for product in self:
            pricelist_item = product.pricelist_item_ids.filtered(
                lambda x: x.pricelist_id.name == 'Tarifa mayorista')
            if pricelist_item:
                product.wholesale_price = product.list_price * (1 - pricelist_item.discount / 100)
            else:
                product.wholesale_price = 0.0
