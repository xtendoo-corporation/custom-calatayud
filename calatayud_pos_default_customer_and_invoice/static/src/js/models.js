/** @odoo-module */

import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { patch } from "@web/core/utils/patch";

/**
 * Patch del modelo PosOrder para:
 * 1. Cliente por defecto y facturación automática
 * 2. Código postal para clientes contado
 * 3. Datos personalizados en recibos
 */
patch(PosOrder.prototype, {
    /**
     * Método que se ejecuta DESPUÉS de añadir la orden al POS
     * En este punto this.pos ya está definido
     */
    setup(_defaultObj, options) {
        super.setup(...arguments);

        // NO hacer nada aquí si this.pos no está disponible
        // Usar _onAfterAdd en su lugar
    },

    /**
     * Hook que se ejecuta después de añadir la orden al POS
     * Aquí this.pos ya está disponible
     */
    _onAfterAdd() {
        if (super._onAfterAdd) {
            super._onAfterAdd(...arguments);
        }

        console.log('🔧 Orden añadida al POS, configurando cliente por defecto');

        // Ahora sí podemos acceder a this.pos de forma segura
        this._setDefaultCustomerAndInvoice();
    },

    /**
     * Establecer cliente por defecto y activar facturación
     */
    _setDefaultCustomerAndInvoice() {
        // Verificar que this.pos existe
        if (!this.pos) {
            console.warn('⚠️ this.pos no está disponible todavía');
            return;
        }

        console.log('🔧 Configurando cliente por defecto y facturación');

        // Obtener el cliente por defecto de la configuración del POS
        const defaultCustomerId = this.pos.config?.res_partner_id;

        if (defaultCustomerId && defaultCustomerId[0]) {
            const defaultCustomer = this.pos.db.get_partner_by_id(defaultCustomerId[0]);

            if (defaultCustomer) {
                this.set_partner(defaultCustomer);
                console.log('✅ Cliente por defecto asignado:', defaultCustomer.name);
            } else {
                console.warn('⚠️ Cliente por defecto no encontrado en la BD');
                this.set_partner(null);
            }
        } else {
            console.log('ℹ️ No hay cliente por defecto configurado');
        }

        // Activar facturación automática
        this.to_invoice = true;
        console.log('📄 Facturación automática activada');
    },

    /**
     * Forzar facturación siempre activa
     */
    set_to_invoice(to_invoice) {
        super.set_to_invoice(true);
        console.log('📝 Facturación forzada a: true');
    },

    /**
     * Exportar datos para impresión del recibo
     */
    export_for_printing() {
        const result = super.export_for_printing(...arguments);

        console.log('📄 Exportando datos para impresión del recibo');

        // Añadir información del partner
        if (this.get_partner()) {
            result.headerData.partner = this.get_partner();
            console.log('👤 Partner añadido:', this.get_partner().name);
        }

        // Añadir código postal si existe
        if (this.walkin_zip_code) {
            result.headerData.walkin_zip_code = this.walkin_zip_code;
            console.log('📮 Código postal añadido:', this.walkin_zip_code);
        }

        // Añadir número de factura si existe
        if (this.account_move) {
            result.headerData.invoice_number = this.account_move;
            console.log('🧾 Número de factura añadido:', this.account_move);
        }

        // Añadir fecha formateada
        if (this.date_order) {
            const orderDate = new Date(this.date_order);
            result.headerData.invoice_date = orderDate.toLocaleDateString('es-ES', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
            console.log('📅 Fecha añadida:', result.headerData.invoice_date);
        }

        // Generar código QR para validación
        if (this.pos && this.pos.generateTicketQRCode) {
            const qrCodeUrl = this.pos.generateTicketQRCode(this);
            if (qrCodeUrl) {
                result.headerData.qr_code_url = qrCodeUrl;
                result.headerData.order_name = this.name;
                console.log('📱 Código QR generado:', qrCodeUrl);
            }
        }

        console.log('✅ Datos del recibo exportados:', result.headerData);

        return result;
    },

    /**
     * Exportar como JSON manteniendo propiedades personalizadas
     */
    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);

        // Forzar facturación
        json.to_invoice = true;

        // Guardar código postal
        if (this.walkin_zip_code) {
            json.walkin_zip_code = this.walkin_zip_code;
        }

        return json;
    },

    /**
     * Inicializar desde JSON
     */
    init_from_JSON(json) {
        super.init_from_JSON(...arguments);

        // Restaurar código postal
        if (json.walkin_zip_code) {
            this.walkin_zip_code = json.walkin_zip_code;
        }

        // Forzar facturación
        this.to_invoice = true;

        // Intentar establecer cliente por defecto si no hay partner
        if (!this.get_partner() && this.pos) {
            this._setDefaultCustomerAndInvoice();
        }
    }
});
