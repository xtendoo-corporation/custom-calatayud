# Copyright (C) 2024 Manuel Calero (<https://xtendoo.es>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def set_multicompany_cost_product_template(self):
        user_company = self.env.company
        standard_price = self.standard_price
        for company in self.env["res.company"].search([("id", "!=", user_company.id)]):
            self.sudo().with_company(company.id).standard_price = standard_price


class ProductProduct(models.Model):
    _inherit = "product.product"

    def set_multicompany_cost_product_product_variant(self):
        user_company = self.env.company
        standard_price = self.standard_price
        for company in self.env["res.company"].search([("id", "!=", user_company.id)]):
            self.sudo().with_company(company.id).standard_price = standard_price

    # Añadimos método puente para evitar error cuando se llame desde vistas erróneas
    def set_multicompany_cost_product_template(self):
        """
        Método puente que redirige a la función correcta para product.product.
        Esto soluciona el error cuando alguna vista heredada llama incorrectamente
        al método de product.template desde product.product.
        """
        return self.set_multicompany_cost_product_product_variant()
