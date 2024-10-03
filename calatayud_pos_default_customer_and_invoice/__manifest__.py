
{
    'name': "POS Default Customer and Invoice | Point of Sales Default Customer and Invoice ",
    'version': '16.0.0.0',
    'category': 'Point of Sale',
    'summary': '',
    'description': """  """,
    'author': 'Abraham Carrasco',
    'website': "",
    'depends': ['base', 'point_of_sale'],
    'data': [
        'views/pos_config.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'calatayud_pos_default_customer_and_invoice/static/src/js/models.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
