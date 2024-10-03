odoo.define('calatayud_pos_default_customer_and_invoice.DefaultCustomer', function (require) {
"use strict";

var models = require('point_of_sale.models');
var utils = require('web.utils');
var { PosGlobalState, Order } = require('point_of_sale.models');
const Registries = require('point_of_sale.Registries');
var core = require('web.core');

const DefaultCustomerOrder = (Order) => class DefaultCustomerOrder extends Order {
    constructor(obj, options) {
        super(...arguments);
        var default_customer = this.pos.config.res_partner_id;
        var default_customer_by_id = this.pos.db.get_partner_by_id(default_customer[0]);
        if(default_customer_by_id){
            this.set_partner(default_customer_by_id);
        } else{
            this.set_partner(null);
        }
        this.to_invoice = true;
    }
}
Registries.Model.extend(Order, DefaultCustomerOrder);
});
