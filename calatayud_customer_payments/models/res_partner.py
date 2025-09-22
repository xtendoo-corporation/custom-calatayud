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
        """Calcula el número total de pagos del cliente"""
        for partner in self:
            if not partner.is_company and partner.parent_id:
                partner.payment_count = 0
                continue

            try:
                # Contar pagos realizados (account.payment)
                payments = self.env['account.payment'].search_count([
                    ('partner_id', '=', partner.id),
                    ('partner_type', '=', 'customer'),
                    ('state', 'in', ['posted', 'sent', 'reconciled'])
                ])

                # Contar facturas pendientes de pago
                pending_invoices = self.env['account.move'].search_count([
                    ('partner_id', '=', partner.id),
                    ('move_type', 'in', ['out_invoice', 'out_refund']),
                    ('payment_state', 'in', ['not_paid', 'partial']),
                    ('state', '=', 'posted')
                ])

                partner.payment_count = payments + pending_invoices
            except Exception:
                partner.payment_count = 0

    def action_view_customer_payments(self):
        """Acción para mostrar los pagos del cliente"""
        self.ensure_one()

        if not self.is_company and self.parent_id:
            return {'type': 'ir.actions.act_window_close'}

        # Obtener pagos realizados
        payments = self.env['account.payment'].search([
            ('partner_id', '=', self.id),
            ('partner_type', '=', 'customer'),
            ('state', 'in', ['posted', 'sent', 'reconciled'])
        ])

        # Obtener facturas pendientes
        pending_invoices = self.env['account.move'].search([
            ('partner_id', '=', self.id),
            ('move_type', 'in', ['out_invoice', 'out_refund']),
            ('payment_state', 'in', ['not_paid', 'partial']),
            ('state', '=', 'posted')
        ])

        # Si solo hay pagos, mostrar vista de pagos
        if payments and not pending_invoices:
            return {
                'name': f'Pagos de {self.name}',
                'type': 'ir.actions.act_window',
                'res_model': 'account.payment',
                'view_mode': 'list,form',
                'domain': [('id', 'in', payments.ids)],
                'context': {
                    'default_partner_id': self.id,
                    'default_partner_type': 'customer',
                    'create': False
                },
            }

        # Si solo hay facturas pendientes, mostrar vista de facturas
        elif pending_invoices and not payments:
            return {
                'name': f'Facturas Pendientes de {self.name}',
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'view_mode': 'list,form',
                'domain': [('id', 'in', pending_invoices.ids)],
                'context': {
                    'default_partner_id': self.id,
                    'create': False
                },
            }

        # Si hay ambos o ninguno, mostrar vista combinada
        else:
            return {
                'name': f'Pagos y Facturas de {self.name}',
                'type': 'ir.actions.act_window',
                'res_model': 'customer.payment.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_partner_id': self.id,
                    'payment_ids': payments.ids,
                    'invoice_ids': pending_invoices.ids,
                },
            }
