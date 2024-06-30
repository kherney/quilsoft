from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    enable_endpoint_hospital = fields.Boolean(config_parameter='vertical_hospital.endpoint')
