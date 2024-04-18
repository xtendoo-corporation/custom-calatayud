# Copyright 2024 Manuel Calero (https://xtendoo.es)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def cron_action_update_standard_price(self):
        print("Cron action run********************************************")
        almacenes_company_id = self.env['res.company'].search([('vat', '=', 'ESB41271206')], limit=1)
        tienda_company_id = self.env['res.company'].search([('vat', '=', 'ESB91823187')], limit=1)

        products_template = self.env['product.template'].search([("company_id", "=", False)])
        for product in products_template:
            almacenes_product = product.with_company(almacenes_company_id)
            tienda_product = product.with_company(tienda_company_id)

            if almacenes_product.standard_price != tienda_product.standard_price:
                tienda_product.standard_price = almacenes_product.standard_price
            if almacenes_product.taxes_id != tienda_product.taxes_id:
                tienda_product.taxes_id = almacenes_product.taxes_id
            if almacenes_product.supplier_taxes_id != tienda_product.supplier_taxes_id:
                tienda_product.supplier_taxes_id = almacenes_product.supplier_taxes_id

            for variant in product.product_variant_ids:
                almacenes_variant = variant.with_company(almacenes_company_id)
                tienda_variant = variant.with_company(tienda_company_id)
                if almacenes_variant.standard_price != tienda_variant.standard_price:
                    tienda_variant.standard_price = almacenes_variant.standard_price
