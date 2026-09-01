from odoo import models, _
from odoo.tools import html_escape


class IrUiView(models.Model):
    _inherit = 'ir.ui.view'

    def _calatayud_fix_stale_website_views(self, keys=None):
        """Restablece las vistas qweb por-website de website_sale que conservan el
        template Odoo 17 (desactualizado tras la migración a Odoo 18) al template
        genérico actual de Odoo 18.

        Criterio: para cada vista por-website activa de website_sale.* (o de las
        `keys` indicadas) que tenga una vista genérica equivalente (misma key,
        website_id NULL), si su arch difiere del genérico se guarda copia de
        seguridad y se restablece.

        Devuelve un dict {view_id: key} con las vistas corregidas.
        """
        View = self.env['ir.ui.view']
        fixed = []

        domain = [
            ('type', '=', 'qweb'),
            ('key', 'like', 'website_sale.%'),
            ('website_id', '!=', False),
            ('active', '=', True),
        ]
        if keys:
            domain[1] = ('key', 'in', keys)

        stale = View.with_context(lang=None).search(domain)

        for view in stale:
            generic = View.with_context(lang=None).search([
                ('key', '=', view.key),
                ('website_id', '=', False),
            ], order='id', limit=1)

            if not generic:
                # Sin vista genérica de referencia: no podemos determinar el estado,
                # la dejamos tal cual.
                continue

            arch = view.arch_db or ''
            generic_arch = generic.arch_db or ''
            if arch == generic_arch:
                continue

            self._calatayud_backup_view_arch(view, arch)
            view.write({'arch_db': generic_arch})
            fixed.append(view.id)

        return fixed

    def _calatayud_backup_view_arch(self, view, arch):
        """Guarda una copia del arch previo de una vista como ir.attachment."""
        Attachment = self.env['ir.attachment']
        name = 'backup_%s_id%d_arch.xml' % (html_escape(view.key or 'view'), view.id)
        existing = Attachment.search([('name', '=', name)], limit=1)
        data = ('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<!-- Backup de la vista %s (id %s, website %s) - previo a '
                'calatayud_website_migration_fix -->\n%s'
                % (view.key, view.id, view.website_id.id, arch))
        vals = {
            'name': name,
            'type': 'binary',
            'mimetype': 'application/xml',
            'raw': data.encode('utf-8'),
            'description': _('Backup del arch de la vista %s antes de la corrección de migración') % view.key,
        }
        if existing:
            existing.write({'raw': vals['raw']})
        else:
            Attachment.create(vals)

    def action_calatayud_fix_stale_website_product_views(self):
        """Método accionable (automatización/action) para lanzar la corrección y
        notificar el resultado."""
        fixed = self._calatayud_fix_stale_website_views()
        if fixed:
            message = _('Se corrigieron %s vista(s) de producto de la web: %s') % (
                len(fixed), ', '.join(str(v) for v in fixed))
            self.env['bus.bus']._sendone('odoo', 'notification', {
                'type': 'user_message',
                'message': message,
            })
        return fixed
