/** @odoo-module */

import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { patch } from "@web/core/utils/patch";

console.log('🟢 Cargando extensión de PosOrder para walkin_zip_code');

patch(PosOrder.prototype, {
    setup(_defaultObj, options) {
        super.setup(...arguments);
        this.walkin_zip_code = this.walkin_zip_code || '';
        console.log('🔵 PosOrder setup - walkin_zip_code:', this.walkin_zip_code);
    },

    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.walkin_zip_code = json.walkin_zip_code || '';
        console.log('🔵 PosOrder init_from_JSON - walkin_zip_code:', this.walkin_zip_code);
    },

    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        json.walkin_zip_code = this.walkin_zip_code || '';
        console.log('📦 PosOrder export_as_JSON - this.walkin_zip_code:', this.walkin_zip_code);
        console.log('📦 PosOrder export_as_JSON - json.walkin_zip_code:', json.walkin_zip_code);
        return json;
    },

    export_for_printing() {
        const result = super.export_for_printing(...arguments);
        result.walkin_zip_code = this.walkin_zip_code || '';
        console.log('🖨️ PosOrder export_for_printing - walkin_zip_code:', this.walkin_zip_code);
        return result;
    },

    set_walkin_zip_code(zip_code) {
        this.walkin_zip_code = zip_code;
        console.log('✅ SET walkin_zip_code:', zip_code);
    },

    get_walkin_zip_code() {
        console.log('📍 GET walkin_zip_code:', this.walkin_zip_code);
        return this.walkin_zip_code;
    },
});

console.log('🟢 Extensión de PosOrder aplicada correctamente con patch');
