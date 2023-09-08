# Copyright 2023 Jaime Millan (https://xtendoo.es)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Wholesale Price",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Jaime Millan (https://xtendoo.es)",
    "category": "Sales",
    "depends":
        [
            "sale_management",
        ],
    "data":
        [
            "security/ir.model.access.csv",
            "views/product_product_tree_view.xml",
        ],
    'installable': True,
    'active': False,
}
