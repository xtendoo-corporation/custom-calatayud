/** @odoo-module */

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { useState } from "@odoo/owl";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { useService } from "@web/core/utils/hooks";

/**
 * Extender las props del ConfirmationDialog
 */
ConfirmationDialog.props = {
    ...ConfirmationDialog.props,
    requireZipCode: { type: Boolean, optional: true },
};

/**
 * Patch del ConfirmationDialog para añadir soporte de código postal
 */
patch(ConfirmationDialog.prototype, {
    setup() {
        super.setup();
        // Si se requiere código postal, añadir estado
        if (this.props.requireZipCode) {
            // Asegurarse de que state existe
            if (!this.state) {
                this.state = useState({});
            }
            // Añadir propiedades para el código postal
            Object.assign(this.state, {
                zipCode: "",
                zipError: ""
            });
        }
    },

    /**
     * Manejar cambios en el input del código postal
     */
    onZipCodeChange(ev) {
        if (this.state && this.props.requireZipCode) {
            this.state.zipCode = ev.target.value;
            this.state.zipError = "";
        }
    },

    /**
     * Validar y confirmar con código postal
     */
    async _confirm() {
        // Si requiere código postal, validar
        if (this.props.requireZipCode && this.state) {
            const zipCode = this.state.zipCode.trim();

            // Validar longitud si se introdujo código postal
            if (zipCode && (zipCode.length < 4 || zipCode.length > 10)) {
                this.state.zipError = _t('El código postal debe tener entre 4 y 10 caracteres.');
                return; // No cerrar el diálogo
            }

            // Ejecutar callback con el código postal
            if (this.props.confirm) {
                try {
                    await this.props.confirm(zipCode || '');
                } catch (error) {
                    console.error('Error en confirm callback:', error);
                }
            }
            this.props.close();
        } else {
            // Comportamiento normal del ConfirmationDialog
            return super._confirm();
        }
    }
});

/**
 * Patch de PaymentScreen para solicitar código postal
 */
patch(PaymentScreen.prototype, {
    setup() {
        super.setup();
        this.dialog = useService("dialog");
        this.notification = useService("notification");
    },

    /**
     * Validar orden y solicitar código postal si es necesario
     */
    async validateOrder(isForceValidate) {
        console.log('🔵 ===== INICIO validateOrder (pos_orders_zip) =====');

        const order = this.currentOrder;
        const partner = order.get_partner();

        // Verificar si es cliente contado
        const partnerName = partner ? (partner.name || '').toUpperCase() : '';
        const isWalkInCustomer = partnerName.includes('CONTADO');

        console.log('📋 Cliente:', partnerName);
        console.log('🔍 Es cliente contado:', isWalkInCustomer);
        console.log('📮 Código postal actual:', order.walkin_zip_code);

        // Si es cliente contado y no tiene código postal, solicitar
        if (isWalkInCustomer && !order.walkin_zip_code) {
            console.log('✅ Mostrando diálogo de código postal');

            try {
                // Usar promesa para esperar la respuesta del usuario
                const zipCode = await new Promise((resolve) => {
                    this.dialog.add(ConfirmationDialog, {
                        title: _t("Código Postal del Cliente"),
                        body: _t("Puede introducir el código postal del cliente para mejorar las estadísticas de ventas."),
                        confirmLabel: _t("Guardar"),
                        cancelLabel: _t("Omitir"),
                        requireZipCode: true, // Flag para activar el campo ZIP
                        confirm: async (zipCode) => {
                            console.log('✅ Usuario confirmó con código postal:', zipCode);
                            resolve(zipCode);
                        },
                        cancel: () => {
                            console.log('⚠️ Usuario canceló el diálogo');
                            resolve('');
                        },
                        close: () => {
                            console.log('❌ Diálogo cerrado');
                            resolve('');
                        },
                    });
                });

                // Guardar el código postal si se proporcionó
                if (zipCode) {
                    order.walkin_zip_code = zipCode;
                    console.log('💾 Código postal guardado en la orden:', zipCode);

                    this.notification.add(
                        _t("Código postal guardado: %s", zipCode),
                        { type: "success" }
                    );
                } else {
                    console.log('ℹ️ No se proporcionó código postal');
                }
            } catch (error) {
                console.error('❌ Error en diálogo de código postal:', error);
            }
        }

        // Continuar con la validación normal del pedido
        console.log('⏭️ Continuando con validación original...');
        const result = await super.validateOrder(isForceValidate);

        console.log('🔵 ===== FIN validateOrder =====');
        return result;
    }
});
