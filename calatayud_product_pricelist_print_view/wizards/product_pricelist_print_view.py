# Copyright (C) 2024 Manuel Calero (<https://xtendoo.es>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api


class ProductPricelistPrint(models.TransientModel):
    _inherit = "product.pricelist.print"

    description_product = fields.Boolean(
        default="True",
        string="Description product",
    )
    product_price_piece = fields.Float(
        compute="_compute_product_price_piece",
    )

    def get_pricelist_min_quantity(self, pricelist):
        self.ensure_one()
        for item in pricelist.item_ids:
            if item.applied_on == "3_global" and item.min_quantity > 0.0:
                return item.min_quantity
        return 1.0

    @api.depends_context("product")
    def _compute_product_price_piece(self):
        product = self.env.context["product"]
        pricelist = self.get_pricelist_to_print()
        price = pricelist._get_product_price(
            product, self.get_pricelist_min_quantity(pricelist), date=self.date
        )
        if self.vat_mode == "vat_excl":
            self.product_price_piece = product.taxes_id.compute_all(price)["total_excluded"]
        elif self.vat_mode == "vat_incl":
            self.product_price_piece = product.taxes_id.compute_all(price)["total_included"]
        else:
            self.product_price_piece = price
