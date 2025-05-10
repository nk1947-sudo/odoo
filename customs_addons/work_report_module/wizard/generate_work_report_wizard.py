from odoo import models, fields
import logging
_logger = logging.getLogger(__name__)
_logger.info("🚀 work.report.template model loaded successfully.")
class GenerateWorkReportWizard(models.TransientModel):
    _name = 'generate.work.report.wizard'
    _description = 'Wizard to generate work report'

    date_from = fields.Date(string="From Date")
    date_to = fields.Date(string="To Date")

    def action_generate(self):
        # You can add logic here to generate reports in batch
        return True
