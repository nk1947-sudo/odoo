from odoo import http
from odoo.http import request
import json
from ..ai_services.ocr_engine import OcrEngine
from ..ai_services.bid_predictor import BidPredictor
from ..ai_services.nlp_extractor import NlpExtractor

class TenderAIApi(http.Controller):

    @http.route('/dawell/ai/analyze', type='json', auth='user')
    def analyze_tender(self, tender_id):
        tender = request.env['tender.management'].browse(tender_id)
        if not tender.exists():
            return {'error': 'Tender not found'}

        ai_result = BidPredictor.full_analysis(tender)
        ai_insight = request.env['tender.ai.insight'].create({
            'tender_id': tender.id,
            **ai_result
        })
        tender.ai_score_id = ai_insight.id
        return {'message': 'AI Insight generated', 'ai_insight_id': ai_insight.id}

    @http.route('/dawell/ai/ocr', type='http', auth='user', methods=['POST'], csrf=False)
    def ocr_upload(self, **kwargs):
        file = kwargs.get('file')
        if not file:
            return request.make_response(json.dumps({'error': 'No file uploaded'}),
                                         headers=[('Content-Type', 'application/json')])
        try:
            file_path = '/tmp/ocr_temp_file'
            with open(file_path, 'wb') as f:
                f.write(file.read())
            result = OcrEngine.extract_from_image(file_path)
        except Exception as e:
            result = {'error': str(e)}

        return request.make_response(json.dumps(result), headers=[('Content-Type', 'application/json')])

    @http.route('/dawell/ai/nlp', type='json', auth='user')
    def extract_nlp(self, text):
        categories = NlpExtractor.extract_categories(text)
        requirements = NlpExtractor.extract_requirements(text)
        return {
            'categories': categories,
            'requirements': requirements
        }