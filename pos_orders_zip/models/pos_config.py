from odoo import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    ask_walkin_zip_code = fields.Boolean(
        string="Solicitar código postal",
        help="Si está marcado, al cobrar al cliente CONTADO se pedirá el "
        "código postal antes de confirmar la venta. Se puede omitir, no es "
        "obligatorio para completar el cobro.",
        default=False,
    )
