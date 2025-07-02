from odoo import http, models
from odoo.http import request
from werkzeug.exceptions import HTTPException
from werkzeug.utils import redirect

class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _auth_method_public(cls):
        res = super()._auth_method_public()
        website = request.env['website'].get_current_website()
        if website.id == 1 and request.httprequest.path in ['/shop'] and not request.session.uid:
            raise HTTPException(response=redirect('/web/access'))
        return res
