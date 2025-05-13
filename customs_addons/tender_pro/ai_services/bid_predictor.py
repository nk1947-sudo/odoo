# ai_services/bid_predictor.py
import random

class BidPredictor:
    @staticmethod
    def predict_win_probability(features):
        # Simulated ML result
        return round(random.uniform(75.0, 95.0), 2)

    @staticmethod
    def suggest_bid_amount(estimated_value):
        return round(estimated_value * random.uniform(0.91, 0.95), 2)

    @staticmethod
    def full_analysis(tender):
        win_prob = BidPredictor.predict_win_probability({
            'dept': tender.department_id.name,
            'value': tender.estimated_value,
            'category': tender.category
        })
        bid_amount = BidPredictor.suggest_bid_amount(tender.estimated_value)

        return {
            'win_probability': win_prob,
            'recommended_bid': bid_amount,
            'score': round(win_prob * 0.98, 2),
            'notes': f"Suggested based on similar {tender.category} projects."
        }
