/** @odoo-module */

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";

/**
 * Extiende PaymentScreen para solicitar código postal
 * cuando el cliente es "cliente contado"
 */
patch(PaymentScreen.prototype, {
    /**
     * Se ejecuta al validar el pedido
     * Intercepta para solicitar código postal si es cliente contado
     */
    async validateOrder(isForceValidate) {
        const order = this.currentOrder;

        // Verificar si es cliente contado (sin partner seleccionado)
        // o si el partner es el cliente genérico del POS
        const isWalkInCustomer = !order.get_partner() ||
                                order.get_partner().id === this.pos.config.default_partner_id[0];

        // Si es cliente contado y no tiene código postal, mostrar popup
        if (isWalkInCustomer && !order.walkin_zip_code) {
            const { confirmed, payload } = await this.popup.add('ZipCodePopup', {
                title: _t('Código Postal'),
                body: _t('¿Desea introducir el código postal del cliente?'),
            });

            if (confirmed && payload) {
                // Guardar el código postal en el pedido
                order.walkin_zip_code = payload;
            }
        }

        // Continuar con la validación normal
        return super.validateOrder(isForceValidate);
    }
});
