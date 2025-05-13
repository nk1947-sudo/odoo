from odoo import models, fields

class TenderAttachment(models.Model):
    _name = 'tender.attachment'
   # _inherit = 'documents.document'
    _description = 'Tender Attachment'

    tender_id = fields.Many2one('tender.management', string='Tender', required=True)
