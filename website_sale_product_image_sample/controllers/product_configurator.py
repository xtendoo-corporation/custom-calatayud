# -*- coding: utf-8 -*-
from odoo import http
from odoo.addons.sale.controllers import product_configurator


# Guardar el método original
_original_get_product_information = product_configurator.SaleProductConfiguratorController._get_product_information


def _get_product_information_override(
    self,
    product_template,
    combination,
    currency,
    pricelist,
    so_date,
    quantity=1,
    product_uom_id=None,
    parent_combination=None,
    **kwargs,
):
    """Override para forzar display_type a 'radio' en todos los atributos."""
    # Print al inicio para verificar que el método se está ejecutando
    print("\n" + "="*80)
    print("ENTRANDO EN MONKEY PATCH DE CALATAYUD")
    print(f"Product Template ID: {product_template.id if product_template else 'None'}")
    print("="*80 + "\n")

    product_uom = http.request.env['uom.uom'].browse(product_uom_id)
    product = product_template._get_variant_for_combination(combination)
    attribute_exclusions = product_template._get_attribute_exclusions(
        parent_combination=parent_combination,
        combination_ids=combination.ids,
    )
    product_or_template = product or product_template

    values = dict(
        product_tmpl_id=product_template.id,
        **self._get_basic_product_information(
            product_or_template,
            pricelist,
            combination,
            quantity=quantity,
            uom=product_uom,
            currency=currency,
            date=so_date,
            **kwargs,
        ),
        quantity=quantity,
        attribute_lines=[dict(
            id=ptal.id,
            attribute=dict(
                **{
                    **ptal.attribute_id.read(['id', 'name', 'display_type'])[0],
                    'display_type': 'radio',  # Forzar siempre a 'radio'
                }
            ),
            attribute_values=[
                dict(
                    **ptav.read(['name', 'html_color', 'image', 'is_custom'])[0],
                    price_extra=self._get_ptav_price_extra(
                        ptav, currency, so_date, product_or_template
                    ),
                ) for ptav in ptal.product_template_value_ids
                if ptav.ptav_active or combination and ptav.id in combination.ids
            ],
            selected_attribute_value_ids=combination.filtered(
                lambda c: ptal in c.attribute_line_id
            ).ids,
            create_variant=ptal.attribute_id.create_variant,
        ) for ptal in product_template.attribute_line_ids],
        exclusions=attribute_exclusions['exclusions'],
        archived_combinations=attribute_exclusions['archived_combinations'],
        parent_exclusions=attribute_exclusions['parent_exclusions'],
    )

    # Imprimir para debug
    print("\n" + "="*80)
    print("PRODUCT CONFIGURATOR - DEBUG - MONKEY PATCH CALATAYUD")
    print(f"Product Template: {product_template.name}")
    print(f"Número de attribute_lines: {len(values.get('attribute_lines', []))}")
    for attr_line in values.get('attribute_lines', []):
        attr = attr_line.get('attribute', {})
        print(f"Attribute: {attr.get('name')} - Display Type: {attr.get('display_type')}")
        for attr_val in attr_line.get('attribute_values', []):
            print(f"  - Value: {attr_val.get('name')} - Image: {bool(attr_val.get('image'))}")
    print("="*80 + "\n")

    # Shouldn't be sent client-side
    values.pop('pricelist_rule_id', None)
    return values


# Aplicar el monkey patch
product_configurator.SaleProductConfiguratorController._get_product_information = _get_product_information_override

print("\n" + "="*80)
print("MONKEY PATCH APLICADO A SaleProductConfiguratorController._get_product_information")
print("="*80 + "\n")
