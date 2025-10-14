odoo.define('pos_orders_zip.ZipCodePopup', function(require) {
    'use strict';

    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');
    const { useRef } = owl;

    class ZipCodePopup extends AbstractAwaitablePopup {
        setup() {
            super.setup();
            this.zipCodeInputRef = useRef('zipcode-input');
        }

        mounted() {
            super.mounted();
            if (this.zipCodeInputRef.el) {
                this.zipCodeInputRef.el.focus();
            }
        }

        getPayload() {
            const zipCode = this.zipCodeInputRef.el ? this.zipCodeInputRef.el.value.trim() : '';
            return zipCode;
        }

        async confirm() {
            const zipCode = this.getPayload();

            // Validación: si no es válido, NO cerrar el popup
            if (zipCode && (zipCode.length < 4 || zipCode.length > 10)) {
                await this.showPopup('ErrorPopup', {
                    title: this.env._t('Código Postal Inválido'),
                    body: this.env._t('El código postal debe tener entre 4 y 10 caracteres.'),
                });
                return; // NO llamar super.confirm() - mantener popup abierto
            }

            // Si pasa la validación, cerrar el popup
            // super.confirm() cierra automáticamente y devuelve {confirmed: true, payload: getPayload()}
            super.confirm();
        }

        cancel() {
            // super.cancel() cierra automáticamente y devuelve {confirmed: false, payload: null}
            super.cancel();
        }

        onKeyPress(event) {
            if (event.key === 'Enter') {
                this.confirm();
            }
        }
    }

    ZipCodePopup.template = 'ZipCodePopup';
    ZipCodePopup.defaultProps = {
        title: 'Código Postal',
        body: '¿Desea introducir el código postal del cliente?',
    };

    Registries.Component.add(ZipCodePopup);

    return ZipCodePopup;
});
