from odoo import models, _
from odoo.tools import html_escape


class IrUiView(models.Model):
    _inherit = 'ir.ui.view'

    def _calatayud_fix_stale_website_product_views(self):
        """Restablece las páginas de producto por-website que conservan el template
        Odoo 17 (llamada a _get_combination_info con pricelist) al template genérico
        actual de Odoo 18.

        Devuelve un listado de las vistas corregidas (o [] si no hay nada que hacer).
        """
        View = self.env['ir.ui.view']

        generic = View.with_context(lang=None).search([
            ('key', '=', 'website_sale.product'),
            ('type', '=', 'qweb'),
            ('website_id', '=', False),
        ], order='id', limit=1)

        if not generic:
            return []

        generic_arch = generic.arch_db

        stale = View.with_context(lang=None).search([
            ('key', '=', 'website_sale.product'),
            ('type', '=', 'qweb'),
            ('website_id', '!=', False),
        ])

        fixed = []
        for view in stale:
            arch = view.arch_db or ''
            # Solo corregimos las que aún conservan la llamada de la era Odoo 17
            if 'pricelist=pricelist' not in arch:
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
        fixed = self._calatayud_fix_stale_website_product_views()
        if fixed:
            message = _('Se corrigieron %s vista(s) de producto de la web: %s') % (
                len(fixed), ', '.join(str(v) for v in fixed))
            self.env['bus.bus']._sendone('odoo', 'notification', {
                'type': 'user_message',
                'message': message,
            })
        return fixed
