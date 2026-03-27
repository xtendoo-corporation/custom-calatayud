{
    'name': 'Website Force Login',
    'version': '1.0',
    'author': 'Guillermo Barcena Lopez, Daniel López Bermúdez',
    'category': 'Website',
    'summary': 'Redirige a los usuarios públicos a la página de login',
    'depends': [
        'website',
    ],
    'installable': True,
    'auto_install': False,
    'data': [
        'views/contact_us.xml',
        'views/templates.xml',
    ],
}
