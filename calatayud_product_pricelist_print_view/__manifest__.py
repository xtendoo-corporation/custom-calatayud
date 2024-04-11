# Copyright 2023 Manuel Calero (https://xtendoo.es)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Calatayud Pricelist Report",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Manuel Calero, Abraham Carrasco (https://xtendoo.es)",
    "category": "Sales",
    "depends":
        [
            "product",
            "product_pricelist_direct_print",
            "sale",
        ],
    "data":
        [
            "wizards/product_pricelist_print_view.xml",
            'security/ir.model.access.csv',
        ],
    'installable': True,
    'active': False,
}
