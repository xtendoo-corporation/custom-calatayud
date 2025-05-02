from odoo import http
from odoo.http import request


class WebsiteSaleCustom(http.Controller):

    @http.route(['/shop/payment/validate/custom'], type='http', auth="public", website=True)
    def payment_validate_custom(self, **post):
        order = request.website.sale_get_order()
        if not order:
            return request.redirect('/shop')

        order.with_context(send_email=True).action_confirm()
        request.website.sale_reset()
        return request.redirect('/shop/confirmation')
