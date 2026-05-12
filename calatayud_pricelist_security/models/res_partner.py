from odoo import api, models

from .security_common import (
    PARTNER_BASIC_PRICELIST_DOMAIN,
    check_basic_user_assignment_allowed,
    format_basic_pricelist_domain,
    has_advanced_pricelist_access,
    set_field_domain_in_arch,
)


class ResPartner(models.Model):
    _inherit = "res.partner"

    def get_view(self, view_id=None, view_type="form", **options):
        result = super().get_view(view_id=view_id, view_type=view_type, **options)
        if view_type != "form" or has_advanced_pricelist_access(self.env):
            return result
        result["arch"] = set_field_domain_in_arch(
            result["arch"],
            "property_product_pricelist",
            format_basic_pricelist_domain(PARTNER_BASIC_PRICELIST_DOMAIN, self.env.company.id),
        )
        return result

    @api.constrains("property_product_pricelist")
    def _check_property_product_pricelist_access(self):
        if has_advanced_pricelist_access(self.env):
            return
        for partner in self:
            check_basic_user_assignment_allowed(partner.sudo().property_product_pricelist)

