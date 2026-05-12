from xml.etree import ElementTree as ET

from odoo import _
from odoo.exceptions import AccessError
from odoo.osv import expression


ADVANCED_PRICELIST_GROUP = "calatayud_pricelist_security.group_pricelist_access"
ODOO_ADVANCED_PRICELIST_GROUP = "product.group_sale_pricelist"
PARTNER_BASIC_PRICELIST_DOMAIN = (
    "['&', ('visible_to_basic_users', '=', True), '|', "
    "('company_id', '=', False), ('company_id', '=', {company_id})]"
)
SALE_ORDER_BASIC_PRICELIST_DOMAIN = (
    "['&', ('visible_to_basic_users', '=', True), '|', "
    "('company_id', '=', False), ('company_id', '=', {company_id})]"
)
BASIC_PRICELIST_DOMAIN = [
    ("visible_to_basic_users", "=", True),
    "|",
    ("company_id", "=", False),
    ("company_id", "=", "__CURRENT_COMPANY_ID__"),
]
BASIC_PRICELIST_ITEM_DOMAIN = [
    ("pricelist_id.visible_to_basic_users", "=", True),
    "|",
    ("pricelist_id.company_id", "=", False),
    ("pricelist_id.company_id", "=", "__CURRENT_COMPANY_ID__"),
]


def has_advanced_pricelist_access(env):
    return env.user.has_group(ADVANCED_PRICELIST_GROUP) or env.user.has_group(
        ODOO_ADVANCED_PRICELIST_GROUP
    )


def check_basic_user_assignment_allowed(pricelists):
    if has_advanced_pricelist_access(pricelists.env):
        return
    current_company = pricelists.env.company
    forbidden = pricelists.sudo().filtered(
        lambda pricelist: not pricelist.visible_to_basic_users
        or bool(pricelist.company_id and pricelist.company_id != current_company)
    )
    if forbidden:
        raise AccessError(
            _(
                "No tienes permisos avanzados para asignar una tarifa que no está "
                "marcada como visible para usuarios básicos o que no pertenece a la compañía activa."
            )
        )


def set_field_domain_in_arch(arch, field_name, domain, predicate=None):
    root = ET.fromstring(arch)
    for node in root.iter("field"):
        if node.attrib.get("name") != field_name:
            continue
        if predicate and not predicate(node):
            continue
        node.attrib["domain"] = domain
    return ET.tostring(root, encoding="unicode")


def format_basic_pricelist_domain(template, company_id):
    return template.format(company_id=company_id)


def domain_for_current_company(domain, current_company_id):
    converted = []
    for token in domain:
        if (
            isinstance(token, tuple)
            and len(token) == 3
            and token[2] == "__CURRENT_COMPANY_ID__"
        ):
            converted.append((token[0], token[1], current_company_id))
        else:
            converted.append(token)
    return converted


def add_basic_visibility_domain(env, domain, basic_domain):
    if has_advanced_pricelist_access(env):
        return domain
    return expression.AND(
        [domain or [], domain_for_current_company(basic_domain, env.company.id)]
    )


