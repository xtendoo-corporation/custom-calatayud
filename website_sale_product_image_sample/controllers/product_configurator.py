# -*- coding: utf-8 -*-
from odoo import http
from odoo.addons.sale.controllers.product_configurator import SaleProductConfiguratorController


class SaleProductConfiguratorControllerCalatayud(SaleProductConfiguratorController):
    
    def _get_product_information(
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
            attribute_lines=[
                dict(
                    id=ptal.id,
                    attribute=dict(
                        **{k: v for k, v in ptal.attribute_id.read(['id', 'name', 'display_type'])[0].items() if k != 'display_type'},
                        display_type='radio',  # Forzado desde módulo custom
                    ),
                    attribute_values=[
                        dict(
                            **ptav.read(['name', 'html_color', 'image', 'is_custom'])[0],
                            price_extra=self._get_ptav_price_extra(
                                ptav, currency, so_date, product_or_template
                            ),
                        )
                        for ptav in ptal.product_template_value_ids
                        if ptav.ptav_active or combination and ptav.id in combination.ids
                    ],
                    selected_attribute_value_ids=combination.filtered(lambda c: ptal in c.attribute_line_id).ids,
                    create_variant=ptal.attribute_id.create_variant,
                )
                for ptal in product_template.attribute_line_ids
            ],
            exclusions=attribute_exclusions['exclusions'],
            archived_combinations=attribute_exclusions['archived_combinations'],
            parent_exclusions=attribute_exclusions['parent_exclusions'],
        )
        values.pop('pricelist_rule_id', None)
        return values

