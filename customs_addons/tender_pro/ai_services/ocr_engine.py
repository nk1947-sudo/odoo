# ai_services/ocr_engine.py
import pytesseract
from PIL import Image
import re

class OcrEngine:
    @staticmethod
    def extract_from_image(image_path):
        try:
            text = pytesseract.image_to_string(Image.open(image_path))
            return OcrEngine._parse_text(text)
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def _parse_text(text):
        # Simulate regex-based extraction
        tender_number = re.search(r'Tender\s+No[:\-]?\s*(\w+-\d+)', text)
        department = re.search(r'Department[:\-]?\s*(.*)', text)
        value = re.search(r'Value[:\-]?\s*₹?([\d,\.]+)', text)
        deadline = re.search(r'Deadline[:\-]?\s*(\d{4}-\d{2}-\d{2})', text)

        return {
            'tender_number': tender_number.group(1) if tender_number else '',
            'department': department.group(1).strip() if department else '',
            'value': value.group(1).replace(',', '') if value else '',
            'deadline': deadline.group(1) if deadline else '',
        }
