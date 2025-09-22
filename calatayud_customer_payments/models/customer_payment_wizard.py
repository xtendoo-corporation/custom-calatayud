from odoo import models, fields, api


class CustomerPaymentWizard(models.TransientModel):
    _name = 'customer.payment.wizard'
    _description = 'Wizard para mostrar pagos del cliente'

    partner_id = fields.Many2one('res.partner', string='Cliente', required=True)
    payment_ids = fields.Many2many('account.payment', string='Pagos Realizados')
    invoice_ids = fields.Many2many('account.move', string='Facturas Pendientes')
    total_paid = fields.Monetary(string='Total Pagado', compute='_compute_totals')
    total_pending = fields.Monetary(string='Total Pendiente', compute='_compute_totals')
    currency_id = fields.Many2one('res.currency', string='Moneda', default=lambda self: self.env.company.currency_id)

    @api.depends('payment_ids', 'invoice_ids')
    def _compute_totals(self):
        for record in self:
            # Sumar pagos realizados
            total_paid = sum(payment.amount for payment in record.payment_ids)
            record.total_paid = total_paid

            # Sumar montos pendientes de las facturas
            total_pending = sum(invoice.amount_residual for invoice in record.invoice_ids)
            record.total_pending = total_pending

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        context = self.env.context

        if context.get('default_partner_id'):
            partner_id = context['default_partner_id']
            res['partner_id'] = partner_id

            if context.get('payment_ids'):
                res['payment_ids'] = [(6, 0, context['payment_ids'])]

            if context.get('invoice_ids'):
                res['invoice_ids'] = [(6, 0, context['invoice_ids'])]

        return res

    def action_view_payments(self):
        """Ver solo los pagos realizados"""
        return {
            'name': f'Pagos Realizados - {self.partner_id.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'account.payment',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.payment_ids.ids)],
            'context': {'create': False},
        }

    def action_view_pending_invoices(self):
        """Ver solo las facturas pendientes"""
        return {
            'name': f'Facturas Pendientes - {self.partner_id.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.invoice_ids.ids)],
            'context': {'create': False},
        }

    def action_create_payment(self):
        """Crear un nuevo pago para las facturas pendientes"""
        if not self.invoice_ids:
            return

        return {
            'name': 'Registrar Pago',
            'type': 'ir.actions.act_window',
            'res_model': 'account.payment.register',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'active_model': 'account.move',
                'active_ids': self.invoice_ids.ids,
                'default_partner_id': self.partner_id.id,
            },
        }
