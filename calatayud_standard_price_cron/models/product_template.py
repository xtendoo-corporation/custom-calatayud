# Copyright 2024 Manuel Calero (https://xtendoo.es)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def cron_action_update_standard_price(self):
        print("/"*50)
        almacenes_company_id = self.env['res.company'].search([('vat', '=', 'ESB41271206')], limit=1)
        tienda_company_id = self.env['res.company'].search([('vat', '=', 'ESB91823187')], limit=1)
        products = self.env['product.template'].search([])
        for product in products:
            almacenes_product = product.with_company(almacenes_company_id)
            tienda_product = product.with_company(tienda_company_id)
            if almacenes_product.standard_price != tienda_product.standard_price:
                tienda_product.standard_price = almacenes_product.standard_price

