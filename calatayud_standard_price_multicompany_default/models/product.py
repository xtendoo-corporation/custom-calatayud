# Copyright (C) 2024 Manuel Calero (<https://xtendoo.es>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from typing import List

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def write(self, vals):
        res = super(ProductTemplate, self).write(vals)
        self.ensure_one()
        user_company = self.env.company
        standard_price = self.standard_price

        print("*" * 80)
        print("user_company", user_company)
        print("standard_price", standard_price)

        obj = self.sudo()

        if obj.env["res.company"].search([("id", "!=", user_company.id)]):
            self.write(
                {
                    "standard_price": [(6, 0, standard_price)],
                }
            )

        return res
#
#     # @api.depends_context('company')
#     @api.depends('product_variant_ids', 'product_variant_ids.standard_price')
#     def _compute_standard_price(self):
#         # Depends on force_company context because standard_price is company_dependent
#         # on the product_product
#         unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
#         for template in unique_variants:
#             template.standard_price = template.product_variant_ids.standard_price
#         for template in (self - unique_variants):
#             template.standard_price = 0.0
#
#     def _set_standard_price(self):
#         for template in self:
#             if len(template.product_variant_ids) == 1:
#                 template.product_variant_ids.standard_price = template.standard_price
#
#     def _search_standard_price(self, operator, value):
#         products = self.env['product.product'].search([('standard_price', operator, value)], limit=None)
#         return [('id', 'in', products.mapped('product_tmpl_id').ids)]
#
#     divergent_company_taxes = fields.Boolean(
#         string="Has divergent cross-company taxes",
#         compute="_compute_divergent_company_taxes",
#         compute_sudo=True,
#         store=True,
#         help=(
#             "Does this product have divergent cross-company taxes? "
#             "(Only for multi-company products)"
#         ),
#     )
#
#     # CAMBIAR TAXES POR STANDARD PRICE
#     @api.depends("company_id", "taxes_id", "supplier_taxes_id")
#     def _compute_divergent_company_taxes(self):
#         """Know if this product has divergent taxes across companies."""
#         all_companies = self.env["res.company"].search(
#             [
#                 # Useful for tests, to avoid pollution
#                 ("id", "not in", self.env.context.get("ignored_company_ids", []))
#             ]
#         )
#         for one in self:
#             one.divergent_company_taxes = False
#             # Skip single-company products
#             if one.company_id:
#                 continue
#             # A unique constraint in account.tax makes it impossible to have
#             # duplicated tax names by company
#             customer_taxes = {
#                 frozenset(tax.name for tax in one.taxes_id if tax.company_id == company)
#                 for company in all_companies
#             }
#             if len(customer_taxes) > 1:
#                 one.divergent_company_taxes = True
#                 continue
#
#             supplier_taxes = {
#                 frozenset(
#                     tax.name
#                     for tax in one.supplier_taxes_id
#                     if tax.company_id == company
#                 )
#                 for company in all_companies
#             }
#             if len(supplier_taxes) > 1:
#                 one.divergent_company_taxes = True
#                 continue
#
#     # CAMBIAR TAXES POR STANDARD PRICE
#     def taxes_by_company(self, field, company, match_tax_ids=None):
#         taxes_ids = []
#         if match_tax_ids is None:
#             taxes_ids = company[field].ids
#         # If None: return default taxes
#         if not match_tax_ids:
#             return taxes_ids
#         AccountTax = self.env["account.tax"]
#         for tax in AccountTax.browse(match_tax_ids):
#             taxes_ids.extend(
#                 AccountTax.search(
#                     [("name", "=", tax.name), ("company_id", "=", company.id)]
#                 ).ids
#             )
#         return taxes_ids
#
#     # CAMBIAR TAXES POR STANDARD PRICE
#     def _delete_product_taxes(
#         self,
#         excl_customer_tax_ids: List[int] = None,
#         excl_supplier_tax_ids: List[int] = None,
#     ):
#         """Delete taxes from product excluding chosen taxes
#
#         :param excl_customer_tax_ids: Excluded customer tax ids
#         :param excl_supplier_tax_ids: Excluded supplier tax ids
#         """
#         tax_where = " AND tax_id NOT IN %s"
#         # Delete customer taxes
#         customer_sql = "DELETE FROM product_taxes_rel WHERE prod_id IN %s"
#         customer_sql_params = [tuple(self.ids)]
#         if excl_customer_tax_ids:
#             customer_sql += tax_where
#             customer_sql_params.append(tuple(excl_customer_tax_ids))
#         self.env.cr.execute(customer_sql + ";", customer_sql_params)
#         # Delete supplier taxes
#         supplier_sql = "DELETE FROM product_supplier_taxes_rel WHERE prod_id IN %s"
#         supplier_sql_params = [tuple(self.ids)]
#         if excl_supplier_tax_ids:
#             supplier_sql += tax_where
#             supplier_sql_params.append(tuple(excl_supplier_tax_ids))
#         self.env.cr.execute(supplier_sql + ";", supplier_sql_params)
#
#     # METODO QUE CONTIENE LO IMPORTANTE
#     def set_multicompany_taxes(self):
#         self.ensure_one()
#         user_company = self.env.company
#         customer_tax = self.taxes_id
#         customer_tax_ids = customer_tax.ids
#         if not customer_tax.filtered(lambda r: r.company_id == user_company):
#             customer_tax_ids = []
#         supplier_tax = self.supplier_taxes_id
#         supplier_tax_ids = supplier_tax.ids
#         if not supplier_tax.filtered(lambda r: r.company_id == user_company):
#             supplier_tax_ids = []
#         obj = self.sudo()
#         default_customer_tax_ids = obj.taxes_by_company(
#             "account_sale_tax_id", user_company
#         )
#         default_supplier_tax_ids = obj.taxes_by_company(
#             "account_purchase_tax_id", user_company
#         )
#         # Clean taxes from other companies (cannot replace it with sudo)
#         self._delete_product_taxes(
#             excl_customer_tax_ids=customer_tax_ids,
#             excl_supplier_tax_ids=supplier_tax_ids,
#         )
#         # Use list() to copy list
#         match_customer_tax_ids = (
#             list(customer_tax_ids)
#             if default_customer_tax_ids != customer_tax_ids
#             else None
#         )
#         match_suplier_tax_ids = (
#             list(supplier_tax_ids)
#             if default_supplier_tax_ids != supplier_tax_ids
#             else None
#         )
#         for company in obj.env["res.company"].search([("id", "!=", user_company.id)]):
#             customer_tax_ids.extend(
#                 obj.taxes_by_company(
#                     "account_sale_tax_id", company, match_customer_tax_ids
#                 )
#             )
#             supplier_tax_ids.extend(
#                 obj.taxes_by_company(
#                     "account_purchase_tax_id", company, match_suplier_tax_ids
#                 )
#             )
#         self.write(
#             {
#                 "taxes_id": [(6, 0, customer_tax_ids)],
#                 "supplier_taxes_id": [(6, 0, supplier_tax_ids)],
#             }
#         )
#
#     @api.model_create_multi
#     def create(self, vals_list):
#         new_products = super().create(vals_list)
#         for product in new_products:
#             product.set_multicompany_taxes()
#         return new_products
#
#
# class ProductProduct(models.Model):
#     _inherit = "product.product"
#
#     def set_multicompany_taxes(self):
#         self.product_tmpl_id.set_multicompany_taxes()
