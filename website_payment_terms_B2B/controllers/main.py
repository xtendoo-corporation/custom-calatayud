from odoo import http
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)


# class WebsiteSaleCustom(http.Controller):
#
#     @http.route(['/shop/payment/validate/custom'], type='http', auth="public", website=True)
#     def payment_validate_custom(self, **post):
#         order = request.website.sale_get_order()
#         if not order:
#             return request.redirect('/shop')
#
#         # Confirmar pedido y enviar correo
#         try:
#             order.with_context(send_email=True).action_confirm()
#         except Exception as e:
#             _logger.error("Error al confirmar el pedido %s: %s", order.id, str(e))
#             return request.redirect('/shop/payment/error')
#
#         # Limpiar el pedido de la sesión
#         request.website.sale_reset()
#         # Eliminar las transacciones de post-procesamiento si existen
#         tx = order.get_portal_last_transaction()
#         if tx:
#             request.env['payment.post.processing.item']._remove_transactions(tx)
#         return request.redirect('/shop/confirmation')

    # @http.route(['/shop/payment/validate/custom'], type='http', auth="public", website=True, sitemap=False)
    # def payment_validate_custom(self, **post):
    #     order = request.website.sale_get_order()
    #
    #     if order:
    #         order.action_confirm()
    #
    #         # Enviar correo de confirmación
    #         template_id = request.env.ref('sale.email_template_edi_sale')
    #         if template_id:
    #             template_id.with_context(force_send=True).send_mail(order.id)
    #
    #         request.website.sale_reset()
    #         return request.redirect('/shop/confirmation')
    #
    #     return request.redirect('/shop')


class WebsiteSaleCustom(http.Controller):

    @http.route(['/shop/payment/validate/custom'], type='http', auth="public", website=True)
    def payment_validate_custom(self, **post):
        order = request.website.sale_get_order()
        if not order:
            return request.redirect('/shop')

        try:
            # Confirmar pedido
            order.action_confirm()

            # Forzar envío de correo para Almacenes Calatayud
            if order.company_id.name == 'Almacenes Calatayud S.L.':
                template_id = request.env.ref('sale.email_template_edi_sale')
                if template_id:
                    _logger.info("Enviando correo para pedido %s de Almacenes Calatayud S.L.", order.name)
                    template_id.with_context(
                        force_send=True,
                        mark_so_as_sent=True
                    ).send_mail(order.id)

        except Exception as e:
            _logger.error("Error al confirmar el pedido %s: %s", order.id, str(e))
            return request.redirect('/shop/payment/error')

        request.website.sale_reset()
        tx = order.get_portal_last_transaction()
        if tx:
            request.env['payment.post.processing.item']._remove_transactions(tx)
        return request.redirect('/shop/confirmation')
