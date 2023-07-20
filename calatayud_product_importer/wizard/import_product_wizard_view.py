# Copyright 2023 Manuel Calero
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

// clase para crear poductos desde un archivo excel

from odoo import api, fields, models


class WizardAccountPaymentOrderNotification(models.TransientModel):
    _name = "wizard.account.payment.order.notification"
    _description = "Wizard Account Payment Order Notification"

    def import_products(self):
        # self.ensure_one()
        # self.order_id.action_send_notification()
        # return True
        pass

