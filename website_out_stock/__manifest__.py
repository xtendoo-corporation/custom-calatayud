{
    'name': 'Website Out of Stock Calatayud',
    'version': '16.0.1.0.0',
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
    ],
    'data': ['views/product_template_stock.xml',],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
