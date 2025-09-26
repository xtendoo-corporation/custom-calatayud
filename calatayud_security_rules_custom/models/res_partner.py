from odoo import models, fields, api
from odoo.exceptions import AccessError

COMPANY_PRICELIST_MAP = {
    1: [1, 15, 14], #Almacenes
    4: [11], #Tienda
}

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.onchange('property_product_pricelist')
    def _onchange_pricelist_permission(self):
        if self.env.user.has_group('calatayud_security_rules_custom.group_administrador_tarifas'):
            return {}

        if self.property_product_pricelist:
            allowed_pricelists = self._get_allowed_pricelists()
            if self.property_product_pricelist not in allowed_pricelists:
                raise AccessError(
                    'No tienes permisos para asignar esta tarifa. '
                    'Contacta con un Administrador de Tarifas.'
                )

    def _get_allowed_pricelists(self):
        """Retorna las tarifas permitidas según la empresa del usuario"""
        Pricelist = self.env['product.pricelist']
        if self.env.user.has_group('calatayud_security_rules_custom.group_administrador_tarifas'):
            return Pricelist.search([])

        user_company = self.env.user.company_id
        company_pricelist_map = COMPANY_PRICELIST_MAP
        allowed_pricelist_ids = company_pricelist_map.get(self.env.company.id, [])
        if allowed_pricelist_ids:
            return Pricelist.browse(allowed_pricelist_ids)

        return Pricelist.browse([])

    @api.constrains('property_product_pricelist')
    def _check_pricelist_permission(self):
        for partner in self:
            if not partner.property_product_pricelist:
                continue
            if self.env.user.has_group('calatayud_security_rules_custom.group_administrador_tarifas'):
                continue

            allowed_pricelists = partner._get_allowed_pricelists()
            if partner.property_product_pricelist not in allowed_pricelists:
                raise AccessError(
                    'No tienes permisos para asignar esta tarifa. '
                    'Solo puedes asignar tarifas específicas de tu empresa.'
                )

    def write(self, vals):

        if 'property_product_pricelist' in vals and vals['property_product_pricelist']:
            if not self.env.user.has_group('calatayud_security_rules_custom.group_administrador_tarifas'):
                Pricelist = self.env['product.pricelist']
                pricelist = Pricelist.browse(vals['property_product_pricelist'])
                allowed_pricelists = self._get_allowed_pricelists()

                if pricelist not in allowed_pricelists:
                    raise AccessError(
                        'No tienes permisos para asignar esta tarifa. '
                        'Solo puedes asignar tarifas específicas de tu empresa.'
                    )

        return super(ResPartner, self).write(vals)


