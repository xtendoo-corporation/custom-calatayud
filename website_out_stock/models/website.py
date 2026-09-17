from odoo import fields, models
from odoo.tools.translate import html_translate


class Website(models.Model):
    _inherit = "website"

    default_out_of_stock_message = fields.Html(
        string="Mensaje predeterminado de sin stock",
        translate=html_translate,
        help="Se muestra en la tienda para cualquier producto sin stock que"
        " no tenga configurado su propio mensaje de falta de existencias.",
    )
