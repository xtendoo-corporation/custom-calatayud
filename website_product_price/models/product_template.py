# -*- coding: utf-8 -*-
from odoo import models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'


    @api.model
    def _price_with_tax_computed(
        self, price, product_taxes, taxes, company_id, pricelist, product, partner
    ):
        website = self.env['website'].get_current_website()
        if website.id == 1:
            return price
        res = super()._price_with_tax_computed(
            price, product_taxes, taxes, company_id, pricelist, product, partner
        )
        return res
