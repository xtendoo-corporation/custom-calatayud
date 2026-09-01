def post_init_hook(env):
    """Al instalar el módulo, corrige las vistas qweb de la web de la era Odoo 17
    que quedaron desactualizadas tras la migración a Odoo 18 (ej. product con
    pricelist, cart con short_cart_summary), restableciéndolas al template genérico
    actual de Odoo 18."""
    env['ir.ui.view']._calatayud_fix_stale_website_views()
