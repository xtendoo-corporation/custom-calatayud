# -*- coding: utf-8 -*-
from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    contrareembolso = fields.Float(
        string='Contrareembolso',
        digits='Product Price',
        help='Importe del contrareembolso'
    )
    numero_bultos = fields.Integer(
        string='Nº Bultos',
        default=1,
        help='Número de bultos del envío'
    )

