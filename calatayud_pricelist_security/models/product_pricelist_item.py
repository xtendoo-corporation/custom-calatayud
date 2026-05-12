from odoo import api, models

from .security_common import BASIC_PRICELIST_ITEM_DOMAIN, add_basic_visibility_domain


class ProductPricelistItem(models.Model):
	_inherit = "product.pricelist.item"

	@api.model
	def _search(self, domain, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
		domain = add_basic_visibility_domain(
			self.env, domain, BASIC_PRICELIST_ITEM_DOMAIN
		)
		return super()._search(
			domain,
			offset=offset,
			limit=limit,
			order=order,
			count=count,
			access_rights_uid=access_rights_uid,
		)

