# Copyright 2023 Camilo Prado
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging
import base64
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
        try:
            decoded_data = base64.decodebytes(import_file)
            book = xlrd.open_workbook(file_contents=decoded_data)
            sheet = book.sheet_by_index(0)
            for row in range(1, sheet.nrows):

                print("sheet.cell_value(row, 1)", sheet.cell_value(row, 1))

                if sheet.cell_value(row, 1):
                    self._create_attribute(sheet, row)
                else:
                    print("create_product_template")
                    self._create_product_template(sheet, row)
                print(row)

        except xlrd.XLRDError:
            raise ValidationError(
                _("Invalid file style, only .xls or .xlsx file allowed")
            )
        except Exception as e:
            raise e

    def _create_product_template(self, sheet, row):
        name = sheet.cell_value(row, 0)
        description_sale = sheet.cell_value(row, 2)
        product_tag = sheet.cell_value(row, 3)
        if not name:
            return
        result = self.env["product.template"].search([("name", "=", name)])
        if result:
            return result
        product_template = {
            'detailed_type': 'product',
            'invoice_policy': 'delivery',
            'name': name,
            'description_sale': description_sale,
        }
        if product_tag:
            product_tag_ids = self._find_or_create_product_tag(product_tag)

            if product_tag_ids:
                product_template['product_tag_ids'] = [(6, 0, product_tag_ids.ids)]

        self.env["product.template"].create(product_template)

    def _find_or_create_product_tag(self, product_tag):
        result = self.env["product.tag"].search([("name", "=", product_tag)])
        if result:
            return result
        result = self.env["product.tag"].create(
            {"name": product_tag}
        )
        return result

    def _create_attribute(self, sheet, row):
        product_attribute_value = sheet.cell_value(row, 1)
        product_attribute = self._find_or_create_product_attribute('Color')
        if not product_attribute:
            return
        self._find_or_create_product_attribute_value(product_attribute, product_attribute_value)

    def _find_or_create_product_attribute(self, product_attribute):
        result = self.env["product.attribute"].search([("name", "=", product_attribute)])
        if result:
            return result
        result = self.env["product.attribute"].create(
            {"name": product_attribute}
        )
        return result

    def _find_or_create_product_attribute_value(self, product_attribute, product_attribute_value):
        product_attribute_id = product_attribute[0].id
        result = self.env["product.attribute.value"].search(
            [
                ("name", "=", product_attribute_value),
                ("attribute_id", "=", product_attribute_id)
            ]
        )
        if result:
            return result
        result = self.env["product.attribute.value"].create(
            {
                "attribute_id": product_attribute_id,
                "name": product_attribute_value,
            }
        )
        return result
