# Copyright (C) 2024 Manuel Calero (<https://xtendoo.es>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def set_multicompany_cost(self):
        user_company = self.env.company
        standard_price = self.standard_price
        for company in self.env["res.company"].search([("id", "!=", user_company.id)]):
            self.sudo().with_company(company.id).standard_price = standard_price



