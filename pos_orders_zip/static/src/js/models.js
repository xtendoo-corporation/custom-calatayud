odoo.define('pos_orders_zip.models', function(require) {
    'use strict';

    const { Order } = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');

    console.log('🟢 Cargando extensión de Order para walkin_zip_code');

    // Patchear el modelo Order en Odoo 16
    const PosOrderZipCode = (Order) => class PosOrderZipCode extends Order {
        constructor() {
            super(...arguments);
            this.walkin_zip_code = this.walkin_zip_code || '';
            console.log('🔵 Order constructor - walkin_zip_code:', this.walkin_zip_code);
        }

        init_from_JSON(json) {
            super.init_from_JSON(...arguments);
            this.walkin_zip_code = json.walkin_zip_code || '';
            console.log('🔵 Order init_from_JSON - walkin_zip_code:', this.walkin_zip_code);
        }

        export_as_JSON() {
            const json = super.export_as_JSON(...arguments);
            json.walkin_zip_code = this.walkin_zip_code || '';
            console.log('📦 Order export_as_JSON - this.walkin_zip_code:', this.walkin_zip_code);
            console.log('📦 Order export_as_JSON - json.walkin_zip_code:', json.walkin_zip_code);
            return json;
        }

        export_for_printing() {
            const result = super.export_for_printing(...arguments);
            result.walkin_zip_code = this.walkin_zip_code || '';
            console.log('🖨️ Order export_for_printing - walkin_zip_code:', this.walkin_zip_code);
            return result;
        }

        set_walkin_zip_code(zip_code) {
            this.walkin_zip_code = zip_code;
            console.log('✅ SET walkin_zip_code:', zip_code);
        }

        get_walkin_zip_code() {
            console.log('📍 GET walkin_zip_code:', this.walkin_zip_code);
            return this.walkin_zip_code;
        }
    };

    Registries.Model.extend(Order, PosOrderZipCode);

    console.log('🟢 Extensión de Order aplicada correctamente con Registries');
});
