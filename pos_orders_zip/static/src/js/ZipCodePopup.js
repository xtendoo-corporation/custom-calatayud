import { Dialog } from "@web/core/dialog/dialog";
import { useService } from "@web/core/utils/hooks";
import { useRef, onMounted } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";

export class ZipCodePopup extends Dialog {
    static template = "pos_orders_zip.ZipCodePopup";
    static props = {
        ...Dialog.props,
        title: { type: String, optional: true },
        body: { type: String, optional: true },
        close: Function,
        confirm: { type: Function, optional: true },
    };

    static defaultProps = {
        ...Dialog.defaultProps,
        title: _t('Código Postal'),
        body: _t('¿Desea introducir el código postal del cliente?'),
    };

    setup() {
        super.setup();
        this.zipCodeInputRef = useRef('zipcode-input');
        this.popup = useService("dialog");

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

    async onConfirm() {
        const zipCode = this.getPayload();

        // Validación: si no es válido, NO cerrar el popup
        if (zipCode && (zipCode.length < 4 || zipCode.length > 10)) {
            this.popup.add(ErrorPopup, {
                title: _t('Código Postal Inválido'),
                body: _t('El código Postal debe tener entre 4 y 10 caracteres.'),
            });
            return; // NO cerrar el dialog
        }

        // Si pasa la validación, cerrar el popup con el resultado
        if (this.props.confirm) {
            this.props.confirm(zipCode);
        }
        this.props.close();
    }

    onCancel() {
        if (this.props.cancel) {
            this.props.cancel();
        }
        this.props.close();
    }

    onKeyPress(event) {
        if (event.key === 'Enter') {
            this.onConfirm();
        }
    }
}
