from odoo import http
from odoo.http import request

class WebsiteLoginFix(http.Controller):
    @http.route('/web/access', type='http', auth='public', website=True)
    def website_login_options(self, **kw):
        values = {}
        return request.render('website_login_fix.login_options_template', values)
