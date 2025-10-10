from odoo import models, fields, api


class PosOrder(models.Model):
    _inherit = 'pos.order'

    walkin_zip_code = fields.Char(
        string='Código Postal (Cliente Contado)',
        help='Código postal capturado para cliente contado',
        index=True
    )

    @api.model
    def _order_fields(self, ui_order):
        """Extender para incluir el campo walkin_zip_code"""
        order_fields = super(PosOrder, self)._order_fields(ui_order)

        # Añadir el código postal si viene en los datos
        if ui_order.get('walkin_zip_code'):
            order_fields['walkin_zip_code'] = ui_order.get('walkin_zip_code')

        return order_fields
