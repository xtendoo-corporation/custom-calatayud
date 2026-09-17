from odoo.http import request
from odoo.tools import is_html_empty

from odoo.addons.website_sale.controllers.main import TableCompute

_original_process = TableCompute.process


def _process_with_out_of_stock_ribbon(self, products, ppg=20, ppr=4):
    """Add the "Sin existencias" ribbon on out-of-stock products in the shop
    grid, unless the product already has its own ribbon configured manually.

    Only applies on websites that have configured their own out-of-stock
    message (Website Settings > Shop - Products > Mensaje de sin stock).
    Websites that leave it empty keep the default Odoo behavior untouched.
    """
    rows = _original_process(self, products, ppg=ppg, ppr=ppr)

    website = request.env['website'].sudo().get_current_website()
    if is_html_empty(website.default_out_of_stock_message):
        return rows

    ribbon = request.env.ref('website_sale.out_of_stock_ribbon', raise_if_not_found=False)
    if ribbon:
        ribbon = ribbon.sudo()
    if not ribbon:
        return rows

    for row in rows:
        for cell in row:
            product = cell.get('product')
            if product and not cell.get('ribbon') and product.sudo()._is_sold_out():
                cell['ribbon'] = ribbon

    return rows


TableCompute.process = _process_with_out_of_stock_ribbon
