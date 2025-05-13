# ai_services/nlp_extractor.py
import spacy

class NlpExtractor:
    _nlp = spacy.blank('en')

    @staticmethod
    def extract_categories(text):
        keywords = ['infrastructure', 'security', 'maintenance', 'software', 'hardware', 'energy']
        matched = [kw.title() for kw in keywords if kw in text.lower()]
        return matched if matched else ['General']

    @staticmethod
    def extract_requirements(text):
        doc = NlpExtractor._nlp(text)
        return [sent.text for sent in doc.sents if 'must' in sent.text.lower() or 'required' in sent.text.lower()]
