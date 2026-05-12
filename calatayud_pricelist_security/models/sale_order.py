from odoo import api, models

from .security_common import (
    SALE_ORDER_BASIC_PRICELIST_DOMAIN,
    check_basic_user_assignment_allowed,
    format_basic_pricelist_domain,
    has_advanced_pricelist_access,
    set_field_domain_in_arch,
)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def get_view(self, view_id=None, view_type="form", **options):
        result = super().get_view(view_id=view_id, view_type=view_type, **options)
        if view_type != "form" or has_advanced_pricelist_access(self.env):
            return result
        result["arch"] = set_field_domain_in_arch(
            result["arch"],
            "pricelist_id",
            format_basic_pricelist_domain(
                SALE_ORDER_BASIC_PRICELIST_DOMAIN, self.env.company.id
            ),
            predicate=lambda node: node.attrib.get("invisible") != "1",
        )
        return result

    @api.constrains("pricelist_id")
    def _check_pricelist_id_access(self):
        if has_advanced_pricelist_access(self.env):
            return
        for order in self:
            check_basic_user_assignment_allowed(order.sudo().pricelist_id)

