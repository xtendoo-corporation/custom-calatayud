/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";

/**
 * Evita que la caja POS entre en suspensión (SaverScreen) por inactividad.
 *
 * En Odoo 18, PosStore.idleTimeout define un temporizador que, tras 5 minutos
 * sin interacción del usuario, muestra la pantalla de reposo (SaverScreen).
 * Al "despertar" la caja se vuelve a la pantalla de login, obligando a
 * re-cargar el POS y a esperar.
 *
 * Al devolver un array vacío se desactiva por completo este temporizador: la
 * caja permanece en su pantalla actual hasta que se cierre manualmente.
 */
patch(PosStore.prototype, {
    get idleTimeout() {
        return [];
    },
});
