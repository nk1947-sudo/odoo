from odoo import models, fields
import logging
_logger = logging.getLogger(__name__)
_logger.info("🚀 work.report.template model loaded successfully.")
class WorkReportTag(models.Model):
    _name = 'work.report.tag'
    _description = 'Work Report Tag'

    name = fields.Char(string='Tag', required=True)
    color = fields.Integer(string='Color Index')
