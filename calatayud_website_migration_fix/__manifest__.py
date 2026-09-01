{
    'name': 'Calatayud Website Migration Fix',
    'version': '18.0.1.0.0',
    'category': 'Website/Website',
    'summary': 'Corrige errores de la web de producto tras migrar de Odoo 17 a 18',
    'description': """
        Módulo de corrección de migración Odoo 17 → 18.

        1) Plantillas de producto por-website desactualizadas:
           Las páginas de producto del sitio web personalizadas por-website
           (con website_id) quedaron guardadas en la base de datos con el template
           XML de Odoo 17, que llama a _get_combination_info(..., pricelist=pricelist).
           En Odoo 18 este método ya no acepta 'pricelist', provocando un TypeError
           al renderizar la página. Un post_init_hook detecta esas vistas obsoletas y
           las restablece al template genérico Odoo 18, guardando copia de seguridad
           del arch anterior como ir.attachment.

        2) Conflicto de condicionales en website_sale_stock.product_availability:
           Los overrides de website_sale_collect (position="attributes" sobre
           'threshold_message') y website_out_stock (position="replace" convirtiendo
           t-elif en t-if) dejan un nodo con dos directivas condicionales (t-if y
           t-elif en el mismo elemento), lo que Owl2 rechaza con
           "Only one conditional branching directive is allowed per node". Este
           módulo reemplaza el nodo con una versión válida de un único condicional.
    """,
    'author': 'Guillermo Barcena Lopez',
    'depends': [
        'base',
        'website',
        'website_sale',
        'website_sale_stock',
        'website_sale_collect',
        'website_out_stock',
    ],
    'data': [],
    'assets': {
        'web.assets_frontend': [
            'calatayud_website_migration_fix/static/src/xml/website_sale_stock_product_availability.xml',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
    'post_init_hook': 'post_init_hook',
    'bootstrap': True,
}
