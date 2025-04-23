from odoo import http, models
from odoo.http import request
from werkzeug.exceptions import HTTPException
from werkzeug.utils import redirect

class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _auth_method_public(cls):
        resultado = super()._auth_method_public()
        if request.httprequest.path in ['/','/contacto', '/novedades', '/home', '/shop','/shop/cart','/contactus'] and not request.session.uid:
            raise HTTPException(response=redirect('/web/login'))
        return resultado
