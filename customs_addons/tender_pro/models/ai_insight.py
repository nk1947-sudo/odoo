from odoo import models, fields

class TenderAIInsight(models.Model):
    _name = 'tender.ai.insight'
    _description = 'AI Insight for Tender'
    _order = 'score desc'

    tender_id = fields.Many2one('tender.management', required=True)
    win_probability = fields.Float(string='Win Probability (%)')
    recommended_bid = fields.Float(string='Recommended Bid (INR)')
    analysis_date = fields.Datetime(default=fields.Datetime.now)
    notes = fields.Text()
    score = fields.Float(help='Overall AI confidence score')