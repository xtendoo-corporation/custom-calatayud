odoo.define('pos_orders_zip.models', function(require) {
    'use strict';

    const models = require('point_of_sale.models');

    // Extender el modelo Order para incluir el campo walkin_zip_code
    const _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        initialize: function(attributes, options) {
            _super_order.initialize.apply(this, arguments);
            this.walkin_zip_code = this.walkin_zip_code || '';
        },

        init_from_JSON: function(json) {
            _super_order.init_from_JSON.apply(this, arguments);
            this.walkin_zip_code = json.walkin_zip_code || '';
        },

        export_as_JSON: function() {
            const json = _super_order.export_as_JSON.apply(this, arguments);
            json.walkin_zip_code = this.walkin_zip_code || '';
            return json;
        },

        export_for_printing: function() {
            const result = _super_order.export_for_printing.apply(this, arguments);
            result.walkin_zip_code = this.walkin_zip_code || '';
            return result;
        },
    });

    return models;
});
