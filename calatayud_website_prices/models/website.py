# -*- coding: utf-8 -*-
from odoo import api, models, fields

class Website(models.Model):
    _inherit = 'website'

    user_public = fields.Boolean(compute='_compute_is_current_user_public', string='User Public', store=True)

    @api.depends('user_id')
    def _compute_is_current_user_public(self):
        for record in self:
            record.user_public = self.env.user.has_group("base.group_public")
