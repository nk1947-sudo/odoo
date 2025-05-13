# wizards/tender_submit_wizard.py
from odoo import models, fields, api

class TenderSubmitWizard(models.TransientModel):
    _name = 'tender.submit.wizard'
    _description = 'Tender Submission Wizard'

    tender_id = fields.Many2one('tender.management', required=True)
    bid_amount = fields.Float('Your Bid Amount', required=True)
    notes = fields.Text('Internal Notes')

    def action_submit_bid(self):
        self.ensure_one()
        self.env['tender.bid'].create({
            'tender_id': self.tender_id.id,
            'bidder_name': self.env.user.name,
            'bid_amount': self.bid_amount,
            'submitted_on': fields.Datetime.now(),
            'outcome': 'submitted'
        })
        self.tender_id.status = 'submitted'
        return {'type': 'ir.actions.act_window_close'}
