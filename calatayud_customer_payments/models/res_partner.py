from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    payment_count = fields.Integer(
        string='Número de Pagos',
        compute='_compute_payment_count',
        store=False
    )

    @api.depends('move_line_ids')
    def _compute_payment_count(self):
        """Calcula el número total de facturas del cliente"""
        for partner in self:
            if not partner.is_company and partner.parent_id:
                partner.payment_count = 0
                continue

            try:
                # Contar TODAS las facturas de cliente (pagadas y pendientes)
                all_invoices = self.env['account.move'].search_count([
                    ('partner_id', '=', partner.id),
                    ('move_type', 'in', ['out_invoice', 'out_refund']),
                    ('state', '=', 'posted')
                ])

                partner.payment_count = all_invoices
            except Exception:
                partner.payment_count = 0

    def action_view_customer_payments(self):
        """Acción para mostrar las facturas del cliente"""
        self.ensure_one()

        if not self.is_company and self.parent_id:
            return {'type': 'ir.actions.act_window_close'}

        # Obtener todas las facturas del cliente
        all_invoices = self.env['account.move'].search([
            ('partner_id', '=', self.id),
            ('move_type', 'in', ['out_invoice', 'out_refund']),
            ('state', '=', 'posted')
        ])

        # Si no hay facturas, no hacer nada
        if not all_invoices:
            return {'type': 'ir.actions.act_window_close'}

        # Mostrar facturas sin filtros automáticos
        return {
            'name': f'Facturas de {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [
                ('id', 'in', all_invoices.ids),
                ('partner_id', '=', self.id),
                ('move_type', 'in', ['out_invoice', 'out_refund']),
                ('state', '=', 'posted')
            ],
            'context': {
                'default_partner_id': self.id,
                'create': False,
            },
        }
