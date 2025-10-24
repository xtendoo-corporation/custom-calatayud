/** @odoo-module **/

import { PartnerList } from "@point_of_sale/app/screens/partner_list/partner_list";
import { patch } from "@web/core/utils/patch";

/**
 * Validates if a partner has a valid name
 * @param {Object} partner - Partner object to validate
 * @returns {boolean} - True if partner has a valid name
 */
function hasValidName(partner) {
    return partner && partner.name && partner.name.trim() !== '';
}

// Patch the PartnerList component
patch(PartnerList.prototype, {
    /**
     * Override getPartners method to filter out partners without valid names
     */
    getPartners() {
        // Call the original method
        const partners = super.getPartners();
        // Filter partners with valid names
        return partners.filter(partner => hasValidName(partner));
    },

    /**
     * Override getNewPartners to filter results from server
     */
    async getNewPartners() {
        // Call the original method
        const result = await super.getNewPartners();
        // Filter partners with valid names
        return result.filter(partner => hasValidName(partner));
    }
});
