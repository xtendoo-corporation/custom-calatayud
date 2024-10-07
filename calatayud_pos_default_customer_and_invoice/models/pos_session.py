import re

from odoo import models, fields, api


class PosSessionLoadFields(models.Model):
    _inherit = 'pos.session'

    def _pos_ui_models_to_load(self):
        result = super()._pos_ui_models_to_load()
        result += [
            'res.config.settings',

        ]
        return result

    def _loader_params_res_config_settings(self):
        return {
            'search_params': {
                'fields': ['invoice_number'],
            },
        }

    def _get_pos_ui_res_config_settings(self, params):
        return self.env['res.config.settings'].search_read(
            **params['search_params'])


class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    def get_invoice(self, id):
        pos_id = self.search([('pos_reference', '=', id)])
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        invoice_id = self.env['account.move'].search(
            [('ref', '=', pos_id.name)])
        return {
            'invoice_id': invoice_id.id,
            'invoice_name': invoice_id.name,
            'base_url': base_url,
        }

