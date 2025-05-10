from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
_logger.info("🚀 work.report.template model loaded successfully.")


class WorkReportTemplate(models.Model):
    _name = 'work.report.template'
    _description = 'Work Report Template'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Name', required=True, tracking=True)
    description = fields.Text(string='Description', tracking=True)
    active = fields.Boolean(string='Active', default=True, tracking=True)
    


    project_id = fields.Many2one('project.project', string='Project', tracking=True)
    task_id = fields.Many2one('project.task', string='Task', domain="[('project_id', '=', project_id)]", tracking=True)
    billable = fields.Boolean(string='Billable by default', default=True)
    tag_ids = fields.Many2many(
        'work.report.tag',
        'work_report_template_tag_rel',
        'template_id',
        'tag_id',
        string='Default Tags'
    )
    category_id = fields.Many2one('work.report.category', string='Category', tracking=True)

    # ✅ NEW: Define line_ids for the template lines
    line_ids = fields.One2many(
        'work.report.template.line',
        'template_id',
        string='Template Lines',
        tracking=True
    )

    def _register_hook(self):
        _logger.info("✅ Model 'work.report.template' registered successfully.")
        return super()._register_hook()


class WorkReportTemplateLine(models.Model):
    _name = 'work.report.template.line'
    _description = 'Work Report Template Line'
    _order = 'sequence'

    template_id = fields.Many2one(
        'work.report.template',
        string='Template',
        ondelete='cascade',
        required=True
    )
    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    project_id = fields.Many2one('project.project', string='Project')
    task_id = fields.Many2one('project.task', string='Task', domain="[('project_id', '=', project_id)]")
    billable = fields.Boolean(string='Billable', default=True)
    default_hours = fields.Float(
        string='Default Hours',
        default=0.0,
        help='Standard expected hours for this template line. Used when generating reports.'
    )
    notes = fields.Text(string='Notes')
