from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSaleStockCustom(WebsiteSale):

    @http.route(['/shop/product/<model("product.template"):product>'], type='http', auth="public", website=True)
    def product(self, product, category='', search='', **kwargs):
        response = super().product(product, category=category, search=search, **kwargs)

        website = request.website
        if website.id == 3 and product.qty_available <= 0:
            response.qcontext['stock_warning'] = "Este producto no está disponible en este momento."

        return response
