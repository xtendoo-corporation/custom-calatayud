from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.variant import WebsiteSaleVariantController


class CustomWebsiteSaleVariantController(WebsiteSaleVariantController):
    @http.route()
    def get_combination_info_website(self, product_template_id, product_id, combination, add_qty, **kw):
        # Tu lógica personalizada aquí
        combination = super(CustomWebsiteSaleVariantController, self).get_combination_info_website(
            product_template_id, product_id, combination, add_qty, **kw
        )
        website = request.env['website'].get_current_website()
        if website.id == 3:
            combination['allow_out_of_stock_order'] = False
        return combination
