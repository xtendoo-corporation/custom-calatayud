import { patch } from "@web/core/utils/patch";
        import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
        import { useService } from "@web/core/utils/hooks";

        patch(PaymentScreen.prototype, {
            setup() {
                super.setup();
                this.orm = useService("orm");
            },

            shouldDownloadInvoice() {
                return false;
            },

            async validateOrder(isForceValidate) {
                const receiptNumber = this.pos.selectedOrder.name;
                const receiptOrder = await super.validateOrder(...arguments);

                try {
                    const result = await this.orm.call(
                        'pos.order',
                        'get_invoice',
                        [receiptNumber]
                    );
                    this.pos.invoice = result.invoice_name;
                } catch (error) {
                    console.error('Error obteniendo factura:', error);
                }

                return receiptOrder;
            }
        });
