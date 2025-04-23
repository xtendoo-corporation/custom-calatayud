from odoo import http
from odoo.http import request

class CustomLoginController(http.Controller):

    @http.route('/mi-pagina-login', type='http', auth='public', website=True)
    def custom_login(self, **kw):
        return request.render('website_login_fix.custom_login_template')

    @http.route('/singup_form', type='http', auth='public', website=True)
    def procesar_formulario(self, **post):
        return request.render('website_login_fix.registro_mayoristas_template')
