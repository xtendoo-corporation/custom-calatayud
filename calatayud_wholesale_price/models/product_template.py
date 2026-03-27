# Copyright 2023 Jaime Millan (https://xtendoo.es)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    wholesale_price = fields.Float(
        string='Tarifa mayorista',
        compute='_compute_wholesale_price',
    )
    wholesale_price_with_tax = fields.Float(
        string='Tarifa mayorista con iva',
        compute='_compute_wholesale_price_with_tax',
    )
    retail_price = fields.Float(
        string='Precio venta al público',
        compute='_compute_retail_price',
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

    def _compute_wholesale_price_with_tax(self):
        self.wholesale_price_with_tax = 0.0
        pricelist_id = self.env['product.pricelist'].search([('name', '=', 'TARIFA MAYORISTA IVA INCLUIDO')], limit=1)
        if not pricelist_id:
            return
        for product_id in self:
            wholesale_price_with_tax = pricelist_id._get_product_price(
                product_id, 1.0, uom=product_id.uom_id, date=fields.Date.today(),
            )
            product_id.wholesale_price_with_tax = wholesale_price_with_tax

    def _compute_retail_price(self):
        self.retail_price = 0.0
        pricelist_id = self.env['product.pricelist'].search([('name', '=', 'PVP')], limit=1)
        if not pricelist_id:
            return
        for product_id in self:
            retail_price = pricelist_id._get_product_price(
                product_id, 1.0, uom=product_id.uom_id, date=fields.Date.today(),
            )
            product_id.retail_price = retail_price
