from xml.etree import ElementTree as ET

from odoo.exceptions import AccessError
from odoo.tests import TransactionCase, new_test_user, tagged


@tagged("post_install", "-at_install")
class TestPricelistSecurity(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.advanced_user = new_test_user(
            cls.env,
            login="pricelist_advanced_user",
            groups="sales_team.group_sale_manager,calatayud_pricelist_security.group_pricelist_access",
            company_id=cls.company.id,
            company_ids=[(6, 0, cls.company.ids)],
        )
        cls.basic_user = new_test_user(
            cls.env,
            login="pricelist_basic_user",
            groups="sales_team.group_sale_manager,product.group_product_pricelist",
            company_id=cls.company.id,
            company_ids=[(6, 0, cls.company.ids)],
        )
        cls.odoo_advanced_user = new_test_user(
            cls.env,
            login="pricelist_odoo_advanced_user",
            groups="sales_team.group_sale_manager,product.group_sale_pricelist",
            company_id=cls.company.id,
            company_ids=[(6, 0, cls.company.ids)],
        )
        cls.settings_user = new_test_user(
            cls.env,
            login="pricelist_settings_user",
            groups="base.group_system,sales_team.group_sale_manager,product.group_product_pricelist",
            company_id=cls.company.id,
            company_ids=[(6, 0, cls.company.ids)],
        )
        cls.other_company = cls.env["res.company"].create(
            {
                "name": "Otra compañía seguridad tarifas",
                "currency_id": cls.company.currency_id.id,
            }
        )
        cls.public_pricelist = cls.env["product.pricelist"].create(
            {
                "name": "Tarifa pública",
                "currency_id": cls.company.currency_id.id,
                "company_id": cls.company.id,
                "visible_to_basic_users": True,
            }
        )
        cls.private_pricelist = cls.env["product.pricelist"].create(
            {
                "name": "Tarifa privada",
                "currency_id": cls.company.currency_id.id,
                "company_id": cls.company.id,
                "visible_to_basic_users": False,
            }
        )
        cls.other_company_public_pricelist = cls.env["product.pricelist"].create(
            {
                "name": "Tarifa pública otra compañía",
                "currency_id": cls.company.currency_id.id,
                "company_id": cls.other_company.id,
                "visible_to_basic_users": True,
            }
        )
        cls.public_item = cls.env["product.pricelist.item"].create(
            {
                "pricelist_id": cls.public_pricelist.id,
                "applied_on": "3_global",
                "compute_price": "fixed",
                "fixed_price": 10.0,
            }
        )
        cls.private_item = cls.env["product.pricelist.item"].create(
            {
                "pricelist_id": cls.private_pricelist.id,
                "applied_on": "3_global",
                "compute_price": "fixed",
                "fixed_price": 20.0,
            }
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Cliente tarifas",
                "company_type": "company",
            }
        )

    def test_basic_user_only_sees_public_pricelists(self):
        pricelist_model = self.env["product.pricelist"].with_user(self.basic_user)
        visible_pricelists = pricelist_model.search([])
        self.assertEqual(visible_pricelists, self.public_pricelist)
        self.assertEqual(
            pricelist_model.name_search("Tarifa pública"),
            [self.public_pricelist.name_get()[0]],
        )
        self.assertEqual(pricelist_model.name_search("Tarifa privada"), [])
        self.assertEqual(
            pricelist_model.name_search("Tarifa pública otra compañía"),
            [],
        )

    def test_basic_user_cannot_see_public_pricelist_from_other_company(self):
        pricelist_model = self.env["product.pricelist"].with_user(self.basic_user)
        self.assertEqual(
            pricelist_model.search_count(
                [("id", "=", self.other_company_public_pricelist.id)]
            ),
            0,
        )

    def test_only_advanced_group_keeps_full_pricelist_access(self):
        advanced_model = self.env["product.pricelist"].with_user(self.advanced_user)
        odoo_advanced_model = self.env["product.pricelist"].with_user(
            self.odoo_advanced_user
        )

        self.assertEqual(
            advanced_model.search_count(
                [("id", "in", [self.public_pricelist.id, self.private_pricelist.id])]
            ),
            2,
        )
        self.assertTrue(advanced_model.name_search("Tarifa privada"))
        self.assertEqual(
            odoo_advanced_model.search_count(
                [("id", "in", [self.public_pricelist.id, self.private_pricelist.id])]
            ),
            2,
        )
        self.assertTrue(odoo_advanced_model.name_search("Tarifa privada"))

        created = advanced_model.create(
            {
                "name": "Tarifa creada por avanzado",
                "currency_id": self.company.currency_id.id,
                "company_id": self.company.id,
            }
        )
        self.assertTrue(created)
        self.assertFalse(created.visible_to_basic_users)
        created.write({"visible_to_basic_users": True})
        self.assertTrue(created.visible_to_basic_users)

    def test_settings_user_without_advanced_group_is_still_basic_for_pricelists(self):
        settings_model = self.env["product.pricelist"].with_user(self.settings_user)
        self.assertEqual(settings_model.search([]), self.public_pricelist)
        self.assertEqual(settings_model.name_search("Tarifa privada"), [])

    def test_basic_user_cannot_manage_pricelists(self):
        pricelist_model = self.env["product.pricelist"].with_user(self.basic_user)
        with self.assertRaises(AccessError):
            pricelist_model.create(
                {
                    "name": "Tarifa bloqueada",
                    "currency_id": self.company.currency_id.id,
                    "company_id": self.company.id,
                }
            )

    def test_basic_user_can_assign_public_pricelist_but_not_private_one(self):
        partner = self.partner.copy({"name": "Cliente asignación básica"})

        partner.with_user(self.basic_user).write(
            {"property_product_pricelist": self.public_pricelist.id}
        )
        self.assertEqual(partner.property_product_pricelist, self.public_pricelist)

        with self.assertRaises(AccessError):
            partner.with_user(self.basic_user).write(
                {"property_product_pricelist": self.private_pricelist.id}
            )

    def test_basic_user_gets_public_fallback_when_partner_has_private_pricelist(self):
        partner = self.partner.copy({"name": "Cliente fallback"})
        partner.with_user(self.advanced_user).write(
            {"property_product_pricelist": self.private_pricelist.id}
        )
        basic_pricelist = self.env["product.pricelist"].with_user(
            self.basic_user
        )._get_partner_pricelist_multi([partner.id])[partner.id]
        advanced_partner = self.env["res.partner"].with_user(self.advanced_user).browse(
            partner.id
        )

        self.assertTrue(basic_pricelist.visible_to_basic_users)
        self.assertNotEqual(basic_pricelist, self.private_pricelist)
        self.assertEqual(
            advanced_partner.property_product_pricelist,
            self.private_pricelist,
        )

    def test_sale_order_pricelist_assignment_follows_same_rule(self):
        partner = self.partner.copy(
            {
                "name": "Cliente pedido",
                "property_product_pricelist": self.public_pricelist.id,
            }
        )
        order = self.env["sale.order"].with_user(self.basic_user).create(
            {
                "partner_id": partner.id,
                "pricelist_id": self.public_pricelist.id,
            }
        )
        self.assertEqual(order.pricelist_id, self.public_pricelist)

        with self.assertRaises(AccessError):
            order.with_user(self.basic_user).write(
                {"pricelist_id": self.private_pricelist.id}
            )

        order.with_user(self.advanced_user).write(
            {"pricelist_id": self.private_pricelist.id}
        )
        self.assertEqual(order.pricelist_id, self.private_pricelist)

    def test_pricelist_items_follow_public_vs_private_visibility(self):
        item_model = self.env["product.pricelist.item"]
        basic_items = item_model.with_user(self.basic_user).search([])
        advanced_items = item_model.with_user(self.advanced_user).search([])

        self.assertIn(self.public_item, basic_items)
        self.assertNotIn(self.private_item, basic_items)
        self.assertIn(self.public_item, advanced_items)
        self.assertIn(self.private_item, advanced_items)

    def test_basic_user_keeps_partner_and_sale_pricelist_selectors_but_not_product_button(self):
        partner_arch = self.env["res.partner"].with_user(self.basic_user).get_view(
            view_id=self.env.ref("base.view_partner_form").id,
            view_type="form",
        )["arch"]
        partner_tree = ET.fromstring(partner_arch)
        partner_fields = [
            node
            for node in partner_tree.iter()
            if node.tag == "field"
            and node.attrib.get("name") == "property_product_pricelist"
        ]
        self.assertTrue(partner_fields)
        self.assertTrue(
            any(
                "visible_to_basic_users" in (node.attrib.get("domain") or "")
                for node in partner_fields
            )
        )
        self.assertTrue(
            any(str(self.company.id) in (node.attrib.get("domain") or "") for node in partner_fields)
        )

        sale_order_arch = self.env["sale.order"].with_user(self.basic_user).get_view(
            view_id=self.env.ref("sale.view_order_form").id,
            view_type="form",
        )["arch"]
        sale_order_tree = ET.fromstring(sale_order_arch)
        sale_order_fields = [
            node
            for node in sale_order_tree.iter()
            if node.tag == "field" and node.attrib.get("name") == "pricelist_id"
        ]
        self.assertTrue(sale_order_fields)
        self.assertTrue(
            any(
                "visible_to_basic_users" in (node.attrib.get("domain") or "")
                for node in sale_order_fields
            )
        )
        self.assertTrue(
            any(str(self.company.id) in (node.attrib.get("domain") or "") for node in sale_order_fields)
        )

        template_arch = self.env["product.template"].with_user(self.basic_user).get_view(
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
        self.assertEqual(template_buttons, [])

