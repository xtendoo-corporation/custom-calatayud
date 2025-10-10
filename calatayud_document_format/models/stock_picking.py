from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    contrareembolso = fields.Float(
        string='Contrareembolso',
        digits='Product Price',
        help='Importe del contrareembolso'
    )
