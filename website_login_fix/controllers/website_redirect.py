from odoo import http
from odoo.http import request

class WebsiteRedirect(http.Controller):
    @http.route('/', type='http', auth="public", website=True)
    def redirect_home(self, **kwargs):
        return request.redirect('https://almacenescalatayud.com/')
