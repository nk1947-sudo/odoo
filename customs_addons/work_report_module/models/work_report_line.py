from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)
_logger.info("✅ work.report.line model registered successfully.")


class WorkReportLine(models.Model):
    _name = 'work.report.line'
    _description = 'Work Report Line'
    _order = 'sequence, id'

    sequence = fields.Integer(string='Sequence', default=10)
    report_id = fields.Many2one(
        'work.report', string='Work Report', required=True, ondelete='cascade'
    )
    name = fields.Char(string='Description', required=True)
    project_id = fields.Many2one('project.project', string='Project')
    task_id = fields.Many2one(
        'project.task',
        string='Task',
        domain="[('project_id', '=', project_id)]"
    )
    hours = fields.Float(string='Hours', required=True, default=0.0)
    billable = fields.Boolean(string='Billable', default=True)
    notes = fields.Text(string='Notes')
    employee_id = fields.Many2one(
        'hr.employee',
        string='Employee',
        related='report_id.employee_id',
        store=True,
        readonly=True,
    )
    date = fields.Date(
        string='Date',
        related='report_id.date',
        store=True,
        readonly=True,
    )

    # — New fields for timesheet linking —
    timesheet_id = fields.Many2one(
        'account.analytic.line',
        string="Timesheet Entry",
        readonly=True,
        copy=False,
    )
    posted = fields.Boolean(
        string="Posted to Timesheet",
        default=False,
    )

    @api.constrains('hours')
    def _check_hours(self):
        for rec in self:
            if rec.hours < 0:
                raise ValidationError(_("Hours must be non-negative."))
            if rec.hours > 24:
                raise ValidationError(_("Hours cannot exceed 24 hours per day."))

    @api.constrains('task_id', 'project_id')
    def _check_task_project(self):
        for rec in self:
            if rec.task_id and rec.task_id.project_id != rec.project_id:
                raise ValidationError(_("The task must belong to the selected project."))

    @api.onchange('project_id')
    def _onchange_project_id(self):
        if self.project_id and self.task_id and self.task_id.project_id != self.project_id:
            self.task_id = False
        return {
            'domain': {
                'task_id': [('project_id', '=', self.project_id.id)]
                if self.project_id else []
            }
        }

    def create_timesheet(self):
        """Create a single analytic line per work report line, avoid duplicates."""
        AnalyticLine = self.env['account.analytic.line']
        for line in self:
            if line.timesheet_id:
                # Already posted once, skip to avoid duplication
                continue

            employee = line.employee_id
            if not employee:
                raise UserError(_("No employee assigned to the report."))
            user = employee.user_id
            if not line.date:
                raise UserError(_("No date specified in the report."))
            if not line.hours:
                raise UserError(_("Hours must be greater than 0 to create a timesheet."))
            if line.billable and not line.project_id:
                raise UserError(_("Billable lines require a project."))

            vals = {
                'name': line.name,
                'date': line.date,
                'unit_amount': line.hours,
                'employee_id': employee.id,
                'user_id': user.id if user else False,
            }
            if line.task_id:
                vals.update({
                    'task_id': line.task_id.id,
                    'project_id': line.task_id.project_id.id,
                })
            elif line.project_id:
                vals['project_id'] = line.project_id.id

            ts = AnalyticLine.create(vals)
            line.timesheet_id = ts.id
            line.posted = True

        return True

    @api.model_create_multi
    def create(self, vals_list):
        """Support batch creation of work report lines"""
        for vals in vals_list:
            if 'sequence' not in vals:
                vals['sequence'] = (
                    self.env['ir.sequence'].next_by_code('work.report.line.sequence')
                    or 10
                )
        return super().create(vals_list)
