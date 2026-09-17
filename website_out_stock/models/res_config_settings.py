from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    website_default_out_of_stock_message = fields.Html(
        related="website_id.default_out_of_stock_message",
        readonly=False,
    )
