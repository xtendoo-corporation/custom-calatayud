# Copyright 2023 Camilo Prado
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging
import base64
import requests
import certifi
import urllib3


import uuid
from ast import literal_eval
from datetime import date, datetime as dt
from io import BytesIO

import xlrd
import xlwt

from odoo import _, fields, api, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare
from odoo.tools.safe_eval import safe_eval

_logger = logging.getLogger(__name__)

try:
    from csv import reader
except (ImportError, IOError) as err:
    _logger.error(err)


class CalatayudProductImport(models.TransientModel):
    _name = "calatayud.product.import"
    _description = "Calatayud Product Import"

    import_file = fields.Binary(string="Import File (*.xlsx)")

    def action_import_file(self):
        """ Process the file chosen in the wizard, create bank statement(s) and go to reconciliation. """
        self.ensure_one()
        if self.import_file:
            self._import_record_data(self.import_file)
        else:
            raise ValidationError(_("Please select Excel file to import"))

    @api.model
    def _import_record_data(self, import_file):
        # try:
        decoded_data = base64.decodebytes(import_file)
        book = xlrd.open_workbook(file_contents=decoded_data)
        sheet = book.sheet_by_index(0)
        product_attribute_color = self._search_or_create_product_attribute('Color')
        for row in range(1, sheet.nrows):
            name = sheet.cell_value(row, 0)
            product_attribute_value = sheet.cell_value(row, 1)
            description_sale = sheet.cell_value(row, 2)
            seller = sheet.cell_value(row, 3)
            product_tags = sheet.cell_value(row, 4)
            categories_ecommerce = sheet.cell_value(row, 5)
            category = sheet.cell_value(row, 6)
            category_webs = sheet.cell_value(row, 7)
            standard_price = sheet.cell_value(row, 8)
            description_ecommerce = sheet.cell_value(row, 9)
            image = sheet.cell_value(row, 10)
            if not name:
                return

            print("*"*80)
            print("procesado:", name)
            print("product_attribute_value:", product_attribute_value)
            print("description_sale:", description_sale)
            print("seller:", seller)
            print("product_tags:", product_tags)
            print("category", category)
            print("categories_ecommerce", categories_ecommerce)
            print("category_webs", category_webs)
            print("standard_price", standard_price)
            print("description_ecommerce", description_ecommerce)
            print("image", image)
            print("*"*80)

            product_template = self._search_or_create_product_template(
                name, description_sale, product_tags, category_webs, categories_ecommerce, description_ecommerce
            )
            if not product_template:
                return

            if seller:
                self._search_or_create_seller_in_product_template(
                    product_template, seller
                )

            product_attribute_color_value = self._search_or_create_product_attribute_value(
                product_attribute_color, product_attribute_value
            )

            if product_attribute_color_value:
                self._search_or_create_product_attribute_line(
                    product_template, product_attribute_color, product_attribute_color_value
                )

            self._update_product_product(
                product_template, product_attribute_value, standard_price, image
            )

        # except xlrd.XLRDError:
        #     raise ValidationError(
        #         _("Invalid file style, only .xls or .xlsx file allowed")
        #     )
        # except Exception as e:
        #     raise e

    def _search_or_create_product_template(
            self, name, description_sale, product_tags, category_webs, categories_ecommerce, description_ecommerce):
        if not name:
            return

        product_template = {
            'detailed_type': 'product',
            'invoice_policy': 'delivery',
            'name': name,
            'description_sale': description_sale,
            'public_description': description_ecommerce,
        }

        product_template['product_tag_ids'] = []

        for product_tag in product_tags.split('; '):
            product_tag_ids = self._search_or_create_product_tag(product_tag)
            if product_tag_ids:
                product_template['product_tag_ids'] += product_tag_ids.ids

        product_template['public_categ_ids'] = []

        for category_ecommerce in categories_ecommerce.split('; '):
            category_web_ids = self._search_or_create_public_categ(category_webs, category_ecommerce)
            if category_web_ids:
                product_template['public_categ_ids'] += category_web_ids.ids

        category_id = self._search_or_create_category(category_webs)
        if category_id:
            product_template['categ_id'] = category_id.id

        result = self.env["product.template"].search([("name", "=", name)])
        if result:
            result.write(product_template)
            return result

        print("*"*80)
        print("product_template", product_template)
        print("*"*80)

        return self.env["product.template"].create(product_template)

    def _search_or_create_category(self, category):
        if not category:
            return
        result = self.env["product.category"].search([("name", "=", category)])
        if result:
            return result
        return self.env["product.category"].create(
            {
                "name": category,
                "parent_id": self.env.ref('product.product_category_all').id,
            }
        )

    def _search_or_create_product_tag(self, product_tag):
        if not product_tag:
            return
        result = self.env["product.tag"].search([("name", "=", product_tag)])
        if result:
            return result
        return self.env["product.tag"].create({"name": product_tag})

    def _search_or_create_public_categ(self, category_web, category_ecommerce):
        if not category_web:
            return
        result_web = self.env["product.public.category"].search([("name", "=", category_web)])
        if not result_web:
            result_web = self.env["product.public.category"].create({"name": category_web})
        if not category_ecommerce:
            return result_web

        result_ecommerce = self.env["product.public.category"].search(
            [
                ("name", "=", category_ecommerce),
                ("parent_id", "=", result_web.id),
            ]
        )
        if not result_ecommerce:
            result_ecommerce = self.env["product.public.category"].create(
                {
                    "name": category_ecommerce,
                    "parent_id": result_web.id,
                }
            )
        return result_ecommerce

    def _search_or_create_product_attribute(self, product_attribute):
        result = self.env["product.attribute"].search([("name", "=", product_attribute)])
        if result:
            return result
        result = self.env["product.attribute"].create(
            {"name": product_attribute}
        )
        return result

    def _search_or_create_product_attribute_value(self, product_attribute_color, product_attribute_value):
        product_attribute_color_id = product_attribute_color[0].id
        result = self.env["product.attribute.value"].search(
            [
                ("attribute_id", "=", product_attribute_color_id),
                ("name", "=", product_attribute_value),
            ]
        )
        if result:
            return result
        return self.env["product.attribute.value"].create(
            {
                "attribute_id": product_attribute_color_id,
                "name": product_attribute_value,
            }
        )

    def _search_or_create_product_attribute_line(
        self, product_template, product_attribute_color, product_attribute_color_value
    ):
        result = self.env["product.template.attribute.line"].search(
            [
                ("product_tmpl_id", "=", product_template.id),
                ("attribute_id", "=", product_attribute_color.id),
                ("value_ids", "in", product_attribute_color_value.id),
            ]
        )
        if result:
            return result

        result = self.env["product.template.attribute.line"].search(
            [
                ("product_tmpl_id", "=", product_template.id),
                ("attribute_id", "=", product_attribute_color.id),
            ]
        )
        if result and product_attribute_color_value not in result.value_ids:
            result.write({
                "value_ids": [(4, product_attribute_color_value.id)]
            })
            return result

        result = self.env["product.template.attribute.line"].create(
            {
                "product_tmpl_id": product_template.id,
                "attribute_id": product_attribute_color.id,
                "value_ids": [(6, 0, [product_attribute_color_value.id])],
            }
        )
        return result

    def _update_product_product(self, product_template, product_attribute_value, standard_price, image):
        for product in product_template:
            product_variant = self.env["product.product"].search(
                [
                    ("product_tmpl_id", "=", product.id),
                    ("product_template_variant_value_ids.name", "=", product_attribute_value),
                ]
            )
            if product_variant:
                product_variant.write({
                    "standard_price": standard_price,
                })
                if image:
                    print("*"*80)
                    print("image: ", image)
                    product_variant.write({
                        'image_1920': base64.b64encode(requests.get(image.strip()).content)
                            .replace(b'\n', b''),
                    })

    def _search_or_create_seller_in_product_template(self, product_template, seller):
        res_partner = self.env["res.partner"].search([("name", "=", seller)])
        if not res_partner:
            res_partner = self.env["res.partner"].create(
                {
                    "name": seller,
                    "supplier_rank": 1,
                }
            )
        product_supplierinfo = self.env["product.supplierinfo"].search(
            [
                ("partner_id", "=", res_partner.id),
                ("product_tmpl_id", "=", product_template.id),
            ]
        )
        if not product_supplierinfo:
            self.env["product.supplierinfo"].create(
                {
                    "partner_id": res_partner.id,
                    "product_tmpl_id": product_template.id,
                }
            )
