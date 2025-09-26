{
    'name': 'Calatayud security_rules_custom',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Control de acceso para asignación de tarifas de venta',
    'description': """
        Módulo que permite controlar quién puede asignar tarifas de venta a contactos.
        Solo usuarios con el grupo 'administrador_tarifas' pueden realizar esta acción.
    """,
    'author': 'Guillermo Bárcena López',
    'depends': ['base', 'sale', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
       # 'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
