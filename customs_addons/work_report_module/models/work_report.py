from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)
_logger.info("🚀 work.report.template model loaded successfully.")


class WorkReport(models.Model):
    _name = 'work.report'
    _description = 'Work Report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'

    name = fields.Char(
        string='Report Reference',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New')
    )

    date = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.context_today
    )

    employee_id = fields.Many2one(
        'hr.employee', string='Employee', required=True
    )

    department_id = fields.Many2one(
        related='employee_id.department_id',
        string='Department',
        store=True
    )

    user_id = fields.Many2one(
        related='employee_id.user_id',
        string='User',
        store=True
    )

    template_id = fields.Many2one(
        'work.report.template',
        string='Template'
    )

    line_ids = fields.One2many('work.report.line', 'report_id', string='Work Lines')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('manager_approval', 'Manager Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft', tracking=True)

    approved_by = fields.Many2one('res.users', string='Approved By')
    approved_date = fields.Datetime(string='Approval Date')
    notes = fields.Text(string='Notes')

    total_hours = fields.Float(compute='_compute_hours', store=True, string='Total Hours')
    billable_hours = fields.Float(compute='_compute_hours', store=True, string='Billable Hours')
    non_billable_hours = fields.Float(compute='_compute_hours', store=True, string='Non-Billable Hours')
    efficiency = fields.Float(compute='_compute_hours', store=True, string='Efficiency (%)')

    project_id = fields.Many2one('project.project', string="Project")
    task_id = fields.Many2one('project.task', string="Task")

    # --------------------------------------------------
    # Creation Logic
    # --------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('work.report') or _('New')

        reports = super().create(vals_list)

        for report in reports:
            if report.template_id:
                for line in report.template_id.line_ids:
                    self.env['work.report.line'].create({
                        'report_id': report.id,
                        'name': line.name,
                        'project_id': line.project_id.id,
                        'task_id': line.task_id.id,
                        'billable': line.billable,
                        'hours': line.default_hours,  # Use the template line's default_hours
                    })
        return reports

    # --------------------------------------------------
    # Computed Fields
    # --------------------------------------------------
    @api.depends('line_ids.hours', 'line_ids.billable')
    def _compute_hours(self):
        for rec in self:
            rec.total_hours = sum(line.hours for line in rec.line_ids)
            rec.billable_hours = sum(line.hours for line in rec.line_ids if line.billable)
            rec.non_billable_hours = rec.total_hours - rec.billable_hours
            rec.efficiency = (rec.billable_hours / rec.total_hours * 100) if rec.total_hours else 0.0

    # --------------------------------------------------
    # Overrides & Transitions
    # --------------------------------------------------
    def write(self, vals):
        res = super().write(vals)
        if 'state' in vals:
            self.env['work.report.notification']._send_status_change_notifications(
                self.env['work.report.notification'].search([('notification_type', '=', 'status_change')]),
                self,
                vals['state']
            )
        return res

    # --------------------------------------------------
    # Actions
    # --------------------------------------------------
    def action_submit(self):
        if not self.line_ids:
            raise UserError(_("You cannot submit an empty report."))
        self.write({'state': 'submitted'})

    def action_manager_approve(self):
        self.write({'state': 'manager_approval'})

    def action_approve(self):
        self.write({
            'state': 'approved',
            'approved_by': self.env.user.id,
            'approved_date': fields.Datetime.now()
        })

    def action_reject(self):
        self.write({'state': 'rejected'})
