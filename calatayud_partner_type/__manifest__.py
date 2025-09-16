{
    'name': 'Partner Type',
    'summary': 'Añade tipo de contacto (profesional/particular)',
    'version': '18.0.1.0.0',
    'category': 'Contact',
    'author': 'Xtendoo Software SLU',
    'website': 'https://www.xtendoo.es',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'contacts',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'wizard/partner_type_change_wizard_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
