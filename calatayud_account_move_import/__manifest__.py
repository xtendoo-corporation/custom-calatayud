{
    "name": "Importador de Asientos Contables",
    "version": "17.0.1.0.0",
    "summary": "Importa apuntes contables desde Excel a la contabilidad de Odoo",
    "category": "Accounting",
    "author": "Xtendoo",
    "website": "https://xtendoo.es",
    "license": "AGPL-3",
    "depends": [
        "account",
        "base",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizards/import_account_move_view.xml",
        "views/menu_views.xml",
    ],
    "demo": [],
    "installable": True,
    "application": False,
    "auto_install": False,
}

