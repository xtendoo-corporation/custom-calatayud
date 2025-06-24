from odoo import api, fields, models


class PartnerTypeChangeWizard(models.TransientModel):
    _name = 'res.partner.type.change.wizard'
    _description = 'Asistente para cambiar el tipo de contacto'

    partner_ids = fields.Many2many(
        'res.partner',
        string='Contactos seleccionados',
        readonly=True,
    )
    partner_type = fields.Selection(
        selection=[
            ('profesional', 'Profesional'),
            ('particular', 'Particular')
        ],
        string="Nuevo Tipo de Contacto",
        required=True,
        help="Seleccione el nuevo tipo de contacto para aplicar a todos los contactos seleccionados.",
    )
    count_partners = fields.Integer(
        string='Número de contactos',
        compute='_compute_count_partners',
    )

    @api.depends('partner_ids')
    def _compute_count_partners(self):
        for wizard in self:
            wizard.count_partners = len(wizard.partner_ids)

    def action_change_partner_type(self):
        self.ensure_one()
        if self.partner_ids and self.partner_type:
            self.partner_ids.write({
                'partner_type': self.partner_type,
            })
        return {'type': 'ir.actions.act_window_close'}
