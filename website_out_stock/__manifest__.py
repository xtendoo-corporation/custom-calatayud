{
    'name': 'Website Out of Stock Calatayud',
    'version': '18.0.1.0.0',
    'category': 'Website/Website',
    'summary': 'Personalización del manejo de productos sin stock en la tienda web',
    'description': """
        Módulo que extiende la funcionalidad de productos sin stock en la tienda web.
    """,
    'author': 'Guillermo Barcena Lopez',
    'depends': [
        'base',
        'website',
        'website_sale',
        'website_sale_stock',
    ],
    'data': ['views/product_template_stock.xml', ],
    'assets': {
        'web.assets_frontend': [
            # Ruta relativa desde la raíz del módulo
            'website_out_stock/static/src/xml/stock_msg_template.xml',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
