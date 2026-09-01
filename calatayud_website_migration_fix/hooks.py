def post_init_hook(env):
    """Al instalar el módulo, corrige las páginas de producto de la web
    que quedaron con el template Odoo 17 (pricelist=pricelist)."""
    env['ir.ui.view']._calatayud_fix_stale_website_product_views()
