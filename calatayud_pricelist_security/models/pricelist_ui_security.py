from xml.etree import ElementTree as ET

from odoo import models


def _has_pricelist_ui_access(recordset):
    return recordset.env.user.has_group(
        "calatayud_pricelist_security.group_pricelist_access"
    ) or recordset.env.user.has_group("base.group_system")


def _iter_with_parent(root):
    for parent in root.iter():
        for child in list(parent):
            yield parent, child


def _remove_by_name(root, tag, name):
    for parent, child in list(_iter_with_parent(root)):
        if child.tag == tag and child.attrib.get("name") == name:
            parent.remove(child)


def _set_invisible_on_sale_pricelist(root):
    for node in root.iter():
        if node.tag == "label" and node.attrib.get("for") == "pricelist_id":
            node.attrib["invisible"] = "1"
            node.attrib.pop("modifiers", None)
        elif node.tag == "div" and node.attrib.get("class") == "o_row":
            if any(
                child.tag == "field" and child.attrib.get("name") == "pricelist_id"
                for child in list(node)
            ):
                node.attrib["invisible"] = "1"
                node.attrib.pop("modifiers", None)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def get_view(self, view_id=None, view_type="form", **options):
        result = super().get_view(view_id=view_id, view_type=view_type, **options)
        if view_type != "form" or _has_pricelist_ui_access(self):
            return result
        arch = ET.fromstring(result["arch"])
        _remove_by_name(arch, "button", "open_pricelist_rules")
        result["arch"] = ET.tostring(arch, encoding="unicode")
        return result


class ProductProduct(models.Model):
    _inherit = "product.product"

    def get_view(self, view_id=None, view_type="form", **options):
        result = super().get_view(view_id=view_id, view_type=view_type, **options)
        if view_type != "form" or _has_pricelist_ui_access(self):
            return result
        arch = ET.fromstring(result["arch"])
        _remove_by_name(arch, "button", "open_pricelist_rules")
        result["arch"] = ET.tostring(arch, encoding="unicode")
        return result


class ResPartner(models.Model):
    _inherit = "res.partner"

    def get_view(self, view_id=None, view_type="form", **options):
        result = super().get_view(view_id=view_id, view_type=view_type, **options)
        if view_type != "form" or _has_pricelist_ui_access(self):
            return result
        arch = ET.fromstring(result["arch"])
        _remove_by_name(arch, "field", "property_product_pricelist")
        _remove_by_name(arch, "div", "parent_pricelists")
        result["arch"] = ET.tostring(arch, encoding="unicode")
        return result


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def get_view(self, view_id=None, view_type="form", **options):
        result = super().get_view(view_id=view_id, view_type=view_type, **options)
        if view_type != "form" or _has_pricelist_ui_access(self):
            return result
        arch = ET.fromstring(result["arch"])
        _set_invisible_on_sale_pricelist(arch)
        result["arch"] = ET.tostring(arch, encoding="unicode")
        return result

