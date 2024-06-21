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
    show_pieces = fields.Boolean(
        default="True",
        string="Print pieces",
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

    def force_pricelist_send(self):
        template_id = self.env.ref(
            "product_pricelist_direct_print.email_template_edi_pricelist"
        ).id
        composer = (
            self.env["mail.compose.message"]
            .with_context(
                default_composition_mode="mass_mail",
                default_notify=True,
                default_res_id=self.id,
                default_model="product.pricelist.print",
                default_template_id=template_id,
                active_ids=self.ids,
            )
            .create({})
        )
        values = composer._onchange_template_id(
            template_id, "mass_mail", "product.pricelist.print", self.id
        )["value"]
        composer.write(values)
        composer.action_send_mail()
