from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    partner_type = fields.Selection(
        selection=[
            ('profesional', 'Profesional'),
            ('particular', 'Particular')
        ],
        string="Tipo de Contacto",
        tracking=True,
        copy=True,
        help="Indica si el contacto es un profesional o un particular",
    )
