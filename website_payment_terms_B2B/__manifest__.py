{
    'name': 'Website Payment Terms B2B',
    'version': '17.0.1.0.0',
    'category': 'Website/Website',
    'summary': 'Términos de pago personalizados para B2B',
    'description': """
        Módulo que extiende la funcionalidad de pago del sitio web para B2B
    """,
    'author': 'Guillermo Barcena Lopez',
    'depends': [
        'website_sale',
        'payment',
    ],
    'data': [
        'views/templates.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
