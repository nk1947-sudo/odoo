from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)
_logger.info("🚀 work.report.template.line model loaded successfully.")

class WorkReportTemplateLine(models.Model):
    _name = 'work.report.template.line'
    _description = 'Work Report Template Line'
    _order = 'sequence, id'

    sequence = fields.Integer(string='Sequence', default=10)

    template_id = fields.Many2one(
        'work.report.template',
        string='Template',
        required=True,
        ondelete='cascade',
        index=True
    )

    name = fields.Char(string='Line Description', required=True)

    project_id = fields.Many2one(
        'project.project',
        string='Project',
        index=True
    )

    task_id = fields.Many2one(
        'project.task',
        string='Task',
        domain="[('project_id', '=', project_id)]",
        index=True
    )

    # Unified field name: use only default_hours everywhere
    default_hours = fields.Float(
        string='Default Hours',
        default=8.0,
        digits=(16, 2)
    )

    billable = fields.Boolean(string='Billable', default=True)

    notes = fields.Text(string='Notes')

    category_id = fields.Many2one(
        'work.report.category',
        string='Category',
        index=True
    )

    def _register_hook(self):
        _logger.info("✅ Model 'work.report.template.line' registered successfully.")
        return super()._register_hook()

    @api.model
    def create_report_lines(self, report):
        for line in report.template_id.line_ids:
            self.env['work.report.line'].create({
                'template_line_id': line.id,
                'project_id': line.project_id.id,
                'task_id': line.task_id.id,
                'hours': line.default_hours,  # Use the unified field
                'billable': line.billable,
                'notes': line.notes,
                'category_id': line.category_id.id,
            })
