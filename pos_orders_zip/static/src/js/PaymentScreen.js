odoo.define('pos_orders_zip.PaymentScreen', function(require) {
    'use strict';

    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');

    /**
     * Extiende PaymentScreen para solicitar código postal
     * cuando el cliente es "cliente contado"
     */
    const ZipCodePaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {

            /**
             * Se ejecuta al validar el pedido
             * Intercepta para solicitar código postal si es cliente contado
             */
            async validateOrder(isForceValidate) {
                const order = this.currentOrder;

                // Verificar si es cliente contado (sin partner seleccionado)
                // o si el partner es el cliente genérico del POS
                const isWalkInCustomer = !order.get_partner() ||
                                        order.get_partner().id === this.env.pos.config.default_partner_id[0];

                // Si es cliente contado y no tiene código postal, mostrar popup
                if (isWalkInCustomer && !order.walkin_zip_code) {
                    const { confirmed, payload } = await this.showPopup('ZipCodePopup', {
                        title: this.env._t('Código Postal'),
                        body: this.env._t('¿Desea introducir el código postal del cliente?'),
                    });

                    if (confirmed && payload) {
                        // Guardar el código postal en el pedido
                        order.walkin_zip_code = payload;
                    }
                }

                // Continuar con la validación normal
                return super.validateOrder(isForceValidate);
            }
        };

    Registries.Component.extend(PaymentScreen, ZipCodePaymentScreen);

    return PaymentScreen;
});
