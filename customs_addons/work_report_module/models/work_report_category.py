from odoo import models, fields
import logging
_logger = logging.getLogger(__name__)
_logger.info("🚀 work.report.template model loaded successfully.")

class WorkReportCategory(models.Model):
    _name = 'work.report.category'
    _description = 'Work Report Category'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(
        string='Name',
        required=True,
        tracking=True
    )

    description = fields.Text(
        string='Description',
        tracking=True
    )

    def _register_hook(self):
        _logger.info("✅ Model 'work.report.category' successfully registered.")
        return super()._register_hook()
