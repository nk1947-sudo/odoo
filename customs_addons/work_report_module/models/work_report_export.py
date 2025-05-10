from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)
_logger.info("✅ work.report.export model loaded successfully.")

# work_report_export.py



class WorkReportExport(models.TransientModel):
    _name = 'work.report.export'
    _description = 'Work Report Export Wizard'

    date_from = fields.Date(string='Start Date', required=True)
    date_to = fields.Date(string='End Date', required=True)
    employee_ids = fields.Many2many('hr.employee', string='Employees')
