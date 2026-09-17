from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.variant import WebsiteSaleVariantController
from odoo.tools import is_html_empty
from markupsafe import Markup


class CustomWebsiteSaleVariantController(WebsiteSaleVariantController):
    @http.route()
    def get_combination_info_website(self, product_template_id, product_id, combination, add_qty, **kw):
        # Tu lógica personalizada aquí
        combination = super(CustomWebsiteSaleVariantController, self).get_combination_info_website(
            product_template_id, product_id, combination, add_qty, **kw
        )
        website = request.env['website'].get_current_website()
        if not is_html_empty(website.default_out_of_stock_message):
            combination['allow_out_of_stock_order'] = True
            combination['show_availability'] = True
            combination['available_threshold'] = 100
            if is_html_empty(combination.get('out_of_stock_message')):
                combination['out_of_stock_message'] = website.default_out_of_stock_message

        return combination
