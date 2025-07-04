from odoo import http
from odoo.http import request
from odoo.tools import logging
_logger = logging.getLogger(__name__)


class WebsiteSaleCustom(http.Controller):

    @http.route(['/shop/payment/validate/custom'], type='http', auth="public", website=True)
    def payment_validate_custom(self, **post):
        order = request.website.sale_get_order()
        if not order:
            return request.redirect('/shop')

        # Confirmar pedido y enviar correo
        try:
            order.with_context(send_email=True).action_confirm()
        except Exception as e:
            _logger.error("Error al confirmar el pedido %s: %s", order.id, str(e))
            return request.redirect('/shop/payment/error')

        # Limpiar el pedido de la sesión
        request.website.sale_reset()
        # Eliminar las transacciones de post-procesamiento si existen
        tx = order.get_portal_last_transaction()
        if tx:
            request.env['payment.post.processing.item']._remove_transactions(tx)
        return request.redirect('/shop/confirmation')
