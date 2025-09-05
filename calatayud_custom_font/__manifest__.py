# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Calatayud - Fuente Montserrat',
    'version': '17.0.1.0.0',
    'category': 'Website',
    'summary': 'Aplica la fuente Montserrat a toda la web',
    'author': 'Xtendoo',
    'website': 'https://xtendoo.es',
    'license': 'AGPL-3',
    'depends': [
        'web',
        'website',
    ],
    'assets': {
        'web.assets_frontend': [
            'calatayud_custom_font/static/src/css/montserrat_font.css',
        ],
        'web.assets_backend': [
            'calatayud_custom_font/static/src/css/montserrat_font.css',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}
