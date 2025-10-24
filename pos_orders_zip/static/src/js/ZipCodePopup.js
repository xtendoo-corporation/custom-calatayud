/** @odoo-module */

import { Component, useRef, onMounted } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";

export class ZipCodePopup extends Component {
    static template = "pos_orders_zip.ZipCodePopup";
    static props = {
        close: Function,
        title: { type: String, optional: true },
        body: { type: String, optional: true },
    };

    setup() {
        this.zipCodeInputRef = useRef('zipcode-input');

        onMounted(() => {
            if (this.zipCodeInputRef.el) {
                this.zipCodeInputRef.el.focus();
            }
        });
    }

    getPayload() {
        const zipCode = this.zipCodeInputRef.el ? this.zipCodeInputRef.el.value.trim() : '';
        return zipCode;
    }

    async confirm() {
        const zipCode = this.getPayload();

        // Validación: si no es válido, NO cerrar el popup
        if (zipCode && (zipCode.length < 4 || zipCode.length > 10)) {
            // Mostrar alerta simple sin cerrar el popup
            alert(_t('El código postal debe tener entre 4 y 10 caracteres.'));
            return; // NO cerrar el dialog
        }

        // Si pasa la validación, cerrar el popup con el resultado
        this.props.close({ confirmed: true, payload: zipCode });
    }

    cancel() {
        // Cerrar sin código postal
        this.props.close({ confirmed: false, payload: null });
    }

    onKeyPress(event) {
        if (event.key === 'Enter') {
            this.confirm();
        }
    }
}
