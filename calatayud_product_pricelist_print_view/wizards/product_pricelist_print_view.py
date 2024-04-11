# Copyright (C) 2024 Manuel Calero (<https://xtendoo.es>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api


class Productpricelistprint(models.Model):
    _name = 'product.pricelist.print.custom'
    _inherit = 'product.pricelist.print'

    description_product = fields.Boolean(string="Description product")
