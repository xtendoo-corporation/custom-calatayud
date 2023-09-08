# Copyright 2023 Jaime Millan (https://xtendoo.es)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    wholesale_price = fields.Float(
        string='Tarifa mayorista',
        compute='_compute_wholesale_price',
    )
    # pricelist_item_ids = fields.One2many(
    #     comodel_name='product.pricelist.item',
    #     inverse_name='product_id',
    #     string='Pricelist Items',
    # )

    def _compute_wholesale_price(self):
        pricelist = self.env['product.pricelist'].search([('name', '=', 'Tarifa mayorista')])
        pricelist_item = pricelist.items_ids[0]
        for product in self:

            print("/"*80)
            print("pricelist", pricelist)
            print("product", product)
            print("/"*80)

            order_date = fields.Date.today()
            qty = 1.0
            uom = product.uom_id
            product.wholesale_price = pricelist_item._compute_price(
                product, qty, uom, order_date, currency=self.currency_id
            )

            # product.wholesale_price = self._get_pricelist_price(pricelist, product)
            # pricelist_item = product.pricelist_item_ids.filtered(
            #     lambda x: x.pricelist_id.name == 'Tarifa mayorista')
            # if pricelist_item:
            #     product.wholesale_price = product.list_price * (1 - pricelist_item.percent_price / 100)
            # else:
            #     product.wholesale_price = 0.0

    def _get_pricelist_price(self, pricelist, product):
        """Compute the price given by the pricelist for the given line information.

        :return: the product sales price in the order currency (without taxes)
        :rtype: float
        """
        self.ensure_one()

        # pricelist_rule = self.pricelist_item_id
        order_date = fields.Date.today()
        # product = self.product_id.with_context(**self._get_product_price_context())
        qty = 1.0
        uom = product.uom_id

        price = pricelist._compute_price(
            product, qty, uom, order_date, currency=self.currency_id)

        print("*"*80)
        print("pricelist", pricelist)
        print("product", product)
        print("price", price)
        print("*"*80)

        return price
