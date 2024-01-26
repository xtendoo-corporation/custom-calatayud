# Copyright 2023 Camilo Prado (https://xtendoo.es)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Importador de productos Calatayud",
    "version": "16.0",
    "author": "Camilo Prado (https://xtendoo.es)",
    "category": "Calatayud",
    "license": "AGPL-3",
    "depends": [
        "product",
        "stock",
        "sale",
        "pos_sale",
        "purchase",
        "website_sale",
        "website_sale_product_description",
    ],
    "data": [
        "wizard/import_product_wizard_view.xml",
        "views/calatayud_product_import_view.xml",
        "security/ir.model.access.csv",
    ],
    'installable': True,
    'active': False,
}
