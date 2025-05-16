from odoo import http
from odoo.http import request

class TenderDashboardController(http.Controller):

    @http.route('/tender/dashboard', type='http', auth='user', website=True)
    def render_dashboard(self, **kwargs):
        Tender = request.env['tender.management'].sudo()
        values = {
            'total_tenders': Tender.search_count([]),
            'active_tenders': Tender.search_count([('status', '=', 'active')]),
            'submitted_tenders': Tender.search_count([('status', '=', 'submitted')]),
            'won_tenders': Tender.search_count([('status', '=', 'won')]),
            'lost_tenders': Tender.search_count([('status', '=', 'lost')]),
        }
        return request.render('tender_pro.TenderDashboard', values)
