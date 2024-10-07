odoo.define('pos_receipt_extend.PaymentScreen', function (require) {
    'use strict';
    var rpc = require('web.rpc')
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');
    const { onMounted } = owl;

    const PosPaymentReceiptExtend = PaymentScreen => class extends PaymentScreen {
        setup() {
        super.setup();
        }
        shouldDownloadInvoice() {
            return false;
        }
         async validateOrder(isForceValidate) {
            var receipt_number = this.env.pos.selectedOrder.name
            var orders = this.env.pos.selectedOrder
            const receipt_order = await super.validateOrder(...arguments);
            const codeWriter = new window.ZXing.BrowserQRCodeSvgWriter();
            const data = this.env.pos.session_orders;
            var length = data.length-1
            var order = data[length]
            var mobile = order.customer_mobile;
            var phone = order.customer_phone;
            var email = order.customer_email;
            var vat = order.customer_vat;
            var address = order.customer_address;
            var name = order.customer_name;
            var number = order.invoice_number;
            var qr_code = order.qr_code;
            var customer_details = order.customer_details;
            var self= this;
            self.env.pos.number = order.invoice_number;
            var self= this;
        rpc.query({
                model: 'pos.order',
                method: 'get_invoice',
                args: [receipt_number]
                }).then(function(result){
                    self.env.pos.invoice  = result.invoice_name
                });
                return receipt_order
         }
         }


       Registries.Component.extend(PaymentScreen, PosPaymentReceiptExtend);

    return PaymentScreen;
       });

