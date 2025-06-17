{
    'name': 'Website Force Login',
    'version': '1.0',
    'author': 'Guillermo Barcena Lopez',
    'category': 'Website',
    'summary': 'Redirige a los usuarios públicos a la página de login',
    'depends': [
        'website',
    ],
    'installable': True,
    'auto_install': False,
    'data': [
        'views/singup_form.xml',
        'views/contact_us.xml',
    ],
}
