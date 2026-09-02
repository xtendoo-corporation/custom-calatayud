/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import {
    RadioProductAttribute,
    ProductConfiguratorPopup,
} from "@point_of_sale/app/store/product_configurator_popup/product_configurator_popup";

/**
 * Renders an attribute line whose `display_type` is `image` (the value added by this
 * module on `product.attribute`) as a set of clickable thumbnails, the same way the
 * website configurator does.
 *
 * It extends `RadioProductAttribute` instead of `BaseProductAttribute` directly because
 * the radio input uses a computed `t-att-value`, so OWL cannot pre-select the default
 * value from the template alone: `RadioProductAttribute` already fixes this in its
 * `onMounted` by manually checking the right `<input>`. We only need a different template.
 *
 * Important: `product.template.attribute.value` has no picture of its own for this
 * feature. As `views/variants.xml` shows for the website side, the thumbnail shown for
 * each value is the *product variant image* that results from picking that value (see
 * `ProductTemplate._get_combination_info_image`). So here we build, once, a plain
 * `value.id -> image url` map for the values of *this* attribute line only, by matching
 * each one against the single loaded POS product variant it identifies on its own
 * (`product_template_variant_value_ids == [value.id]`, the case this feature is meant
 * for: one varying attribute picking a distinct photo per value).
 *
 * This is built synchronously in `setup()`, once, into a plain `Map` - not computed
 * lazily from a getter re-evaluated during render - precisely so that later re-renders
 * (e.g. every click, which makes `ProductConfiguratorPopup` recompute the selected
 * variant and re-render its children) can never end up rebuilding it against a
 * momentarily-inconsistent reactive snapshot and losing the thumbnails.
 */
export class ImageProductAttribute extends RadioProductAttribute {
    static template = "website_sale_product_image_sample.ImageProductAttribute";

    setup() {
        super.setup();
        this.pos = usePos();
        this.imageUrlByValueId = this._buildImageUrlIndex();
    }

    _buildImageUrlIndex() {
        const index = new Map();
        try {
            const wantedIds = new Set((this.values || []).map((value) => value.id));
            for (const product of this.pos.models["product.product"].getAll()) {
                const ids = product.raw?.product_template_variant_value_ids;
                if (ids && ids.length === 1 && wantedIds.has(ids[0])) {
                    index.set(ids[0], `/web/image/product.product/${product.id}/image_128`);
                }
            }
        } catch (e) {
            console.warn(
                "website_sale_product_image_sample: could not build variant image index",
                e
            );
        }
        return index;
    }

    getVariantImageUrl(value) {
        return this.imageUrlByValueId.get(value.id) || false;
    }
}

// Register the new component so the (patched) `ProductConfiguratorPopup` template can
// use it for `display_type == 'image'`. No extra data needs to be loaded: the product
// variants and their `image_128` used by `getVariantImageUrl` above are already part of
// the regular POS product data.
patch(ProductConfiguratorPopup, {
    components: {
        ...ProductConfiguratorPopup.components,
        ImageProductAttribute,
    },
});
