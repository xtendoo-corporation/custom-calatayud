{
    'name': 'Customer Payments',
    'version': '1.0.0',
    'category': 'Accounting',
    'summary': 'Smart button para ver pagos de clientes',
    'description': """
        Módulo que agrega un smart button en la vista de clientes
        para mostrar todos los pagos (pendientes y realizados) de ese cliente.
    """,
    'author': 'Guillermo Bárcena López',
    'depends': ['base', 'account'],
    'data': [
        'views/customer_effects.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
