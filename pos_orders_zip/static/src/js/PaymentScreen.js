/** @odoo-module */

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { useService } from "@web/core/utils/hooks";
import { Component, useState } from "@odoo/owl";

/**
 * Extiende ConfirmationDialog para añadir un campo de entrada
 */
class ZipCodeConfirmationDialog extends ConfirmationDialog {
    static template = "pos_orders_zip.ZipCodeConfirmationDialog";

    setup() {
        super.setup();
        this.state = useState({ zipCode: "" });
    }

    _confirm() {
        const zipCode = this.state.zipCode.trim();

        if (zipCode && (zipCode.length < 4 || zipCode.length > 10)) {
            alert(_t('El código postal debe tener entre 4 y 10 caracteres.'));
            return;
        }

        // Pasar el código postal al callback confirm
        if (this.props.confirm) {
            this.props.confirm(zipCode || '');
        }
        this.props.close();
    }
}

/**
 * Extiende PaymentScreen para solicitar código postal
 */
patch(PaymentScreen.prototype, {
    setup() {
        super.setup();
        this.dialog = useService("dialog");
        this.notification = useService("notification");
    },

    async validateOrder(isForceValidate) {
        console.log('🔵 ===== INICIO validateOrder (pos_orders_zip) =====');

        const order = this.currentOrder;
        const partner = order.get_partner();

        // Verificar si es cliente contado
        const partnerName = partner ? (partner.name || '').toUpperCase() : '';
        const isWalkInCustomer = partnerName.includes('CONTADO');

        // Si es cliente contado y no tiene código postal
        if (isWalkInCustomer && !order.walkin_zip_code) {
            console.log('✅ Mostrando diálogo de código postal');

            // Usar promesa para esperar la respuesta del usuario
            await new Promise((resolve) => {
                this.dialog.add(ZipCodeConfirmationDialog, {
                    title: _t("Código Postal"),
                    body: _t("¿Desea introducir el código postal del cliente?"),
                    confirmLabel: _t("Guardar"),
                    cancelLabel: _t("Omitir"),
                    confirm: (zipCode) => {
                        if (zipCode) {
                            order.walkin_zip_code = zipCode;
                            console.log('✅ Código postal guardado:', zipCode);
                            this.notification.add(
                                _t("Código postal guardado: %s", zipCode),
                                { type: "success" }
                            );
                        }
                        resolve();
                    },
                    cancel: () => {
                        console.log('⚠️ Usuario canceló el diálogo');
                        resolve();
                    },
                    close: () => resolve(),
                });
            });
        }

        // Continuar con la validación normal
        const result = await super.validateOrder(isForceValidate);
        console.log('🔵 ===== FIN validateOrder =====');

        return result;
    }
});
