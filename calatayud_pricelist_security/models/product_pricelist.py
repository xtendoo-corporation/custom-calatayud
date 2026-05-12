from odoo import api, fields, models

from .security_common import (
    BASIC_PRICELIST_DOMAIN,
    add_basic_visibility_domain,
    has_advanced_pricelist_access,
)


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    visible_to_basic_users = fields.Boolean(
        string="Visible para usuarios básicos",
        default=False,
        help=(
            "Si está activado, los usuarios sin acceso avanzado a tarifas podrán ver "
            "y seleccionar esta tarifa en contactos y pedidos de venta."
        ),
    )

    @api.model
    def _has_advanced_pricelist_access(self):
        return has_advanced_pricelist_access(self.env)

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        domain = add_basic_visibility_domain(
            self.env, domain, BASIC_PRICELIST_DOMAIN
        )
        return super()._search(
            domain,
            offset=offset,
            limit=limit,
            order=order,
            count=count,
            access_rights_uid=access_rights_uid,
        )

    def _get_partner_pricelist_multi_filter_hook(self):
        if self._has_advanced_pricelist_access():
            return super()._get_partner_pricelist_multi_filter_hook()
        current_company = self.env.company
        allowed_ids = self.sudo().filtered(
            lambda pricelist: pricelist.active
            and pricelist.visible_to_basic_users
            and (not pricelist.company_id or pricelist.company_id == current_company)
        ).ids
        return self.browse(allowed_ids)

