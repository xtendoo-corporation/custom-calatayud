from xml.etree import ElementTree as ET

from odoo.exceptions import AccessError
from odoo.tests import TransactionCase, new_test_user, tagged


@tagged("post_install", "-at_install")
class TestPricelistSecurity(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.pricelist_group = cls.env.ref(
            "calatayud_pricelist_security.group_pricelist_access"
        )
        cls.allowed_user = new_test_user(
            cls.env,
            login="pricelist_allowed_user",
            groups="base.group_user,calatayud_pricelist_security.group_pricelist_access",
            company_id=cls.company.id,
            company_ids=[(6, 0, cls.company.ids)],
        )
        cls.denied_user = new_test_user(
            cls.env,
            login="pricelist_denied_user",
            groups="base.group_user",
            company_id=cls.company.id,
            company_ids=[(6, 0, cls.company.ids)],
        )
        cls.denied_sales_manager = new_test_user(
            cls.env,
            login="pricelist_denied_sales_manager",
            groups="sales_team.group_sale_manager",
            company_id=cls.company.id,
            company_ids=[(6, 0, cls.company.ids)],
        )
        cls.denied_standard_pricelist_user = new_test_user(
            cls.env,
            login="pricelist_denied_standard_pricelist_user",
            groups="sales_team.group_sale_manager,product.group_product_pricelist",
            company_id=cls.company.id,
            company_ids=[(6, 0, cls.company.ids)],
        )
        cls.admin_user = cls.env.ref("base.user_admin")
        cls.pricelist = cls.env["product.pricelist"].create(
            {
                "name": "Tarifa de prueba seguridad",
                "currency_id": cls.company.currency_id.id,
                "company_id": cls.company.id,
            }
        )

    def test_denied_user_cannot_read_or_create_pricelists(self):
        pricelist_model = self.env["product.pricelist"].with_user(self.denied_user)
        self.assertEqual(pricelist_model.search_count([]), 0)
        self.assertEqual(pricelist_model.name_search("Tarifa de prueba seguridad"), [])
        with self.assertRaises(AccessError):
            self.pricelist.with_user(self.denied_user).read(["name"])
        with self.assertRaises(AccessError):
            pricelist_model.create(
                {
                    "name": "Tarifa bloqueada",
                    "currency_id": self.company.currency_id.id,
                    "company_id": self.company.id,
                }
            )

    def test_denied_sales_manager_cannot_read_or_create_pricelists(self):
        pricelist_model = self.env["product.pricelist"].with_user(
            self.denied_sales_manager
        )
        self.assertEqual(pricelist_model.search_count([]), 0)
        self.assertEqual(pricelist_model.name_search("Tarifa de prueba seguridad"), [])
        with self.assertRaises(AccessError):
            self.pricelist.with_user(self.denied_sales_manager).read(["name"])
        with self.assertRaises(AccessError):
            pricelist_model.create(
                {
                    "name": "Tarifa gerente bloqueada",
                    "currency_id": self.company.currency_id.id,
                    "company_id": self.company.id,
                }
            )

    def test_allowed_user_can_manage_pricelists(self):
        pricelist_model = self.env["product.pricelist"].with_user(self.allowed_user)
        self.assertGreaterEqual(pricelist_model.search_count([]), 1)
        self.assertTrue(pricelist_model.name_search("Tarifa de prueba seguridad"))
        pricelist = pricelist_model.create(
            {
                "name": "Tarifa permitida",
                "currency_id": self.company.currency_id.id,
                "company_id": self.company.id,
            }
        )
        self.assertEqual(pricelist.name, "Tarifa permitida")
        pricelist.write({"name": "Tarifa permitida editada"})
        self.assertEqual(pricelist.name, "Tarifa permitida editada")

    def test_admin_user_keeps_access_to_pricelists(self):
        pricelist_model = self.env["product.pricelist"].with_user(self.admin_user)
        self.assertGreaterEqual(pricelist_model.search_count([]), 1)
        self.assertTrue(pricelist_model.name_search("Tarifa de prueba seguridad"))
        pricelist = pricelist_model.create(
            {
                "name": "Tarifa admin permitida",
                "currency_id": self.company.currency_id.id,
                "company_id": self.company.id,
            }
        )
        self.assertEqual(pricelist.name, "Tarifa admin permitida")

    def test_standard_pricelist_group_does_not_expose_pricelist_ui(self):
        user = self.denied_standard_pricelist_user

        template_arch = self.env["product.template"].with_user(user).get_view(
            view_id=self.env.ref("product.product_template_form_view").id,
            view_type="form",
        )["arch"]
        template_tree = ET.fromstring(template_arch)
        template_buttons = [
            node
            for node in template_tree.iter()
            if node.tag == "button"
            and node.attrib.get("name") == "open_pricelist_rules"
        ]
        self.assertEqual(
            len(template_buttons),
            0,
        )

        product_arch = self.env["product.product"].with_user(user).get_view(
            view_id=self.env.ref("product.product_normal_form_view").id,
            view_type="form",
        )["arch"]
        product_tree = ET.fromstring(product_arch)
        product_buttons = [
            node
            for node in product_tree.iter()
            if node.tag == "button"
            and node.attrib.get("name") == "open_pricelist_rules"
        ]
        self.assertEqual(
            len(product_buttons),
            0,
        )

        sale_order_arch = self.env["sale.order"].with_user(user).get_view(
            view_id=self.env.ref("sale.view_order_form").id,
            view_type="form",
        )["arch"]
        sale_order_tree = ET.fromstring(sale_order_arch)
        sale_nodes = []
        for node in sale_order_tree.iter():
            if node.tag == "label" and node.attrib.get("for") == "pricelist_id":
                sale_nodes.append(node)
            elif node.tag == "div" and node.attrib.get("class") == "o_row":
                if any(
                    child.tag == "field" and child.attrib.get("name") == "pricelist_id"
                    for child in list(node)
                ):
                    sale_nodes.append(node)
        self.assertTrue(sale_nodes)
        for node in sale_nodes:
            self.assertEqual(node.attrib.get("invisible"), "1")

    def test_pricelist_items_follow_same_security(self):
        item_model = self.env["product.pricelist.item"]
        denied_item_model = item_model.with_user(self.denied_sales_manager)
        self.assertEqual(denied_item_model.search_count([]), 0)
        allowed_item = item_model.with_user(self.allowed_user).create(
            {
                "pricelist_id": self.pricelist.id,
                "applied_on": "3_global",
                "compute_price": "fixed",
                "fixed_price": 10.0,
            }
        )
        self.assertTrue(bool(allowed_item))
        self.assertEqual(
            item_model.with_user(self.allowed_user).search_count(
                [("id", "=", allowed_item.id)]
            ),
            1,
        )
        self.assertEqual(
            denied_item_model.search_count([("id", "=", allowed_item.id)]),
            0,
        )
        self.assertEqual(denied_item_model.search_count([]), 0)
        with self.assertRaises(AccessError):
            allowed_item.with_user(self.denied_sales_manager).read(["fixed_price"])
        with self.assertRaises(AccessError):
            denied_item_model.create(
                {
                    "pricelist_id": self.pricelist.id,
                    "applied_on": "3_global",
                    "compute_price": "fixed",
                    "fixed_price": 12.0,
                }
            )

