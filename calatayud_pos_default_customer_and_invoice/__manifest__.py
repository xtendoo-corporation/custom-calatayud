{
    'name': "POS Default Customer and Invoice | Point of Sales Default Customer and Invoice ",
    'version': '16.0.0.0',
    'category': 'Point of Sale',
    'summary': '',
    'description': """  """,
    'author': 'Abraham Carrasco',
    'website': "",
    'depends': ['point_of_sale', 'base', 'sale', 'account'],
    'data': [
        'views/pos_config.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'calatayud_pos_default_customer_and_invoice/static/src/js/models.js',
            'calatayud_pos_default_customer_and_invoice/static/src/js/payment.js',
            'calatayud_pos_default_customer_and_invoice/static/src/js/pos_order_receipt.js',
            'calatayud_pos_default_customer_and_invoice/static/src/xml/pos_receipt_inherit.xml',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
