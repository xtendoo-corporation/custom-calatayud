odoo.define('pos_filter_partner.PartnerListScreen', function(require) {
    'use strict';

    const PartnerListScreen = require('point_of_sale.PartnerListScreen');
    const Registries = require('point_of_sale.Registries');

    function hasValidName(partner) {
        return partner && partner.name && partner.name.trim() !== '';
    }

    const PosFilterPartnerListScreen = (PartnerListScreen) =>
        class extends PartnerListScreen {

            get partners() {
                let res = super.partners;
                return res.filter(partner => hasValidName(partner));
            }

            async getNewPartners() {
                let result = await super.getNewPartners();
                return result.filter(partner => hasValidName(partner));
            }
        };

    Registries.Component.extend(PartnerListScreen, PosFilterPartnerListScreen);

    return PartnerListScreen;
});
