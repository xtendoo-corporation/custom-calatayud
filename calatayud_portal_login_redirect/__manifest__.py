{
    'name': 'Calatayud Portal Login Redirect to Website',
    'version': '18.0.1.0.0',
    'category': 'Website/Website',
    'summary': 'Los usuarios de portal, al iniciar sesión, aterrizan en la tienda en vez de en "Mi cuenta"',
    'description': """
        Por defecto, `website.controllers.main.Website._login_redirect` envía a
        cualquier usuario no interno (portal) a `/my` justo después de iniciar
        sesión. Este módulo cambia ese destino a `/` (la home de la web, que ya
        resuelve `website.Website.index()` a la portada/tienda configurada),
        dejando intacto el comportamiento para usuarios internos (que siguen
        yendo a `/odoo` como siempre).

        Un usuario de portal puede seguir accediendo a "Mi cuenta" en cualquier
        momento desde el menú de usuario; este cambio solo afecta a dónde
        aterriza justo tras el login cuando no se pidió una redirección
        explícita (parámetro `redirect`).
    """,
    'author': 'Guillermo Barcena Lopez',
    'depends': [
        'website',
    ],
    'data': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
