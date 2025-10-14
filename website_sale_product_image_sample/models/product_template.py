from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _get_combination_info_image(self, combination_info):
        if combination_info and combination_info.get("product_id"):
            product = (
                self.env["product.product"].sudo().browse(combination_info["product_id"])
            )
            return self.env["website"].image_url(product, "image_256", size=256)
        return ""

    def get_single_product_variant(self):
        res = super().get_single_product_variant()

        # Si el producto tiene atributos tipo imagen, forzar apertura del configurador

        has_image_attributes = any(
            line.attribute_id.display_type == 'image'
            for line in self.attribute_line_ids
        )

        # Si hay una sola variante, pero se necesita mostrar imágenes, vaciamos 'res'
        # para forzar que el configurador se abra en las líneas de pedido.
        print(f"{'*'*100}{has_image_attributes}{'*'*100}")
        if has_image_attributes:
            print(f"[DEBUG] get_single_product_variant result: {res} PERSONLIZADO 2")
            return {}

        return res
