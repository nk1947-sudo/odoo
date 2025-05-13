from odoo import models, fields, api

class Tender(models.Model):
    _name = 'tender.management'
    _description = 'Tender'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'title'
    _order = 'deadline desc'
    _check_company_auto = True

    title = fields.Char(required=True, tracking=True)
    reference = fields.Char(required=True, copy=False, readonly=True, default='New')
    description = fields.Text()
    department_id = fields.Many2one('tender.department', required=True)
    category = fields.Selection([
        ('works', 'Works'),
        ('goods', 'Goods'),
        ('services', 'Services'),
        ('consultancy', 'Consultancy')
    ], required=True)
    estimated_value = fields.Float(string='Estimated Value (INR)', tracking=True)
    deadline = fields.Datetime(required=True, tracking=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('won', 'Won'),
        ('lost', 'Lost'),
        ('cancelled', 'Cancelled')
    ], default='draft', tracking=True)
    bid_ids = fields.One2many('tender.bid', 'tender_id', string='Bids')
    attachment_ids = fields.One2many('tender.attachment', 'tender_id')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, index=True)
    ai_score_id = fields.Many2one('tender.ai.insight', string='AI Insight')

    @api.model
    def create(self, vals):
        if vals.get('reference', 'New') == 'New':
            vals['reference'] = self.env['ir.sequence'].next_by_code('tender.management') or 'New'
        return super(Tender, self).create(vals)
