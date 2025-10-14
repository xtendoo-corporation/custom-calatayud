/** @odoo-module **/
import { registry } from "@web/core/registry";

const ProductTemplateAttributeLineImage = {
    template: "website_sale_product_image_sample.ProductTemplateAttributeLineImage",
};

registry.category("web.template").add(
    "ProductTemplateAttributeLine-image", // display_type='image'
    ProductTemplateAttributeLineImage
);
