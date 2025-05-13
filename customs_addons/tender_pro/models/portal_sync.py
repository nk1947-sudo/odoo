from odoo import models, fields

class TenderPortalSync(models.Model):
    _name = 'tender.portal.sync'
    _description = 'Portal Sync Log'
    _order = 'sync_date desc'

    portal = fields.Selection([('gem', 'GeM'), ('cppp', 'CPPP')], required=True)
    sync_date = fields.Datetime(default=fields.Datetime.now)
    items_synced = fields.Text()
    duration = fields.Float(help='Duration in seconds')
    status = fields.Selection([
        ('success', 'Success'),
        ('failed', 'Failed')
    ], default='success')
    message = fields.Text()
