# -*- coding: utf-8 -*-
{
    'name': 'Calatayud POS Migration Fix',
    'version': '18.0.1.0.0',
    'category': 'Point of Sale',
    'summary': 'Evita que la caja POS entre en suspensión (SaverScreen) por inactividad',
    'description': """
        Este módulo corrige el comportamiento del Punto de Venta (POS) tras la
        migración a Odoo 18: por defecto, la caja entra en un modo de reposo
        (SaverScreen) tras 5 minutos de inactividad, lo que obligaba a las
        clientas a re-cargar la caja y esperar a que volviera a estar operativa.

        Con este módulo se desactiva el temporizador de inactividad del POS,
        de modo que la caja permanece en su pantalla actual mientras no se
        cierre manualmente.
    """,
    'author': 'Xtendoo',
    'website': '',
    'license': 'LGPL-3',
    'depends': ['point_of_sale'],
    'data': [],
    'assets': {
        'point_of_sale._assets_pos': [
            'calatayud_pos_migration_fix/static/src/js/pos_no_sleep.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
