/** @odoo-module */

import { registry } from "@web/core/registry";
import { ZipCodePopup } from "./ZipCodePopup";

// Registrar el popup en el registro de popups del POS
registry.category("pos_popups").add("ZipCodePopup", ZipCodePopup);
