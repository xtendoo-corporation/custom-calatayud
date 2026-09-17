from odoo.addons.website.controllers.main import Website
from odoo.http import request


class WebsitePortalLoginRedirect(Website):

    def _login_redirect(self, uid, redirect=None):
        """After login, send portal users to the website homepage instead of
        "/my", unless an explicit redirect was requested. Internal users keep
        going to the backend as usual."""
        if not redirect and request.params.get('login_success'):
            if not request.env['res.users'].browse(uid)._is_internal():
                redirect = '/'
        return super()._login_redirect(uid, redirect=redirect)
