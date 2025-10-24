# -*- coding: utf-8 -*-
{
    'name': 'xtendoo pos-order zip',
    'version': '18.0.1.0.0',
    'category': 'Point of Sale',
    'summary': 'Captura código postal de clientes contado en POS',
    'description': """
        Módulo que añade funcionalidad para capturar el código postal
        cuando se realiza una venta con cliente contado.

    """,
    'author': 'Guillermo Barcena Lopez',
    'depends': ['point_of_sale'],
    'data': [
        'views/pos_order_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_orders_zip/static/src/js/models.js',
            'pos_orders_zip/static/src/js/PaymentScreen.js',
            'pos_orders_zip/static/src/xml/**/*',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
