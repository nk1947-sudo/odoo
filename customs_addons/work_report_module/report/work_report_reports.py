from odoo import models
import logging

_logger = logging.getLogger(__name__)
_logger.info("🚀 report.work_report.report_work_report_pdf model loaded successfully.")

class WorkReportPDFReport(models.AbstractModel):
    _name = 'report.work_report.report_work_report_pdf'
    _description = 'Work Report PDF Export'

    def _get_report_values(self, docids, data=None):
        """
        Prepares the data dictionary for QWeb PDF rendering.
        This function is triggered by ir.actions.report linked to work.report.
        """
        docs = self.env['work.report'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'work.report',
            'docs': docs,
            'data': data or {},
        }
