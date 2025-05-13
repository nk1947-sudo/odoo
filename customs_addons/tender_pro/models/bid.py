from odoo import models, fields

class TenderBid(models.Model):
    _name = 'tender.bid'
    _description = 'Tender Bid'

    tender_id = fields.Many2one('tender.management', string='Tender', required=True)
    bidder_name = fields.Char(string='Bidder Name', required=True)
    bid_amount = fields.Float(string='Bid Amount', required=True)
    submitted_on = fields.Datetime(string='Submitted On', required=True)
    outcome = fields.Selection([
        ('won', 'Won'),
        ('lost', 'Lost'),
        ('pending', 'Pending')
    ], string='Outcome', default='pending')
