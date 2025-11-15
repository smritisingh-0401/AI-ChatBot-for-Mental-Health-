from sklearn.ensemble import RandomForestClassifier
import numpy as np
from datetime import datetime

# PHQ-9 Questions (standard depression screening tool)
PHQ9_QUESTIONS = [
    "1. Little interest or pleasure in doing things?",
    "2. Feeling down, depressed, or hopeless?",
    "3. Trouble falling or staying asleep, or sleeping too much?",
    "4. Feeling tired or having little energy?",
    "5. Poor appetite or overeating?",
    "6. Feeling bad about yourself or that you're a failure?",
    "7. Trouble concentrating on things?",
    "8. Moving or speaking so slowly (or so fast) that others noticed?",
    "9. Thoughts that you'd be better off dead or hurting yourself?"
]

# Response options with scores (0-3 for each question)
RESPONSE_OPTIONS = {
    "not at all": 0,
    "several days": 1,
    "more than half": 2,
    "nearly every day": 3
}

class DepressionDetector:
    """
    Detects depression severity based on PHQ-9 questionnaire scores
    """
    
    def __init__(self):
        """Initialize the depression detection model"""
        # Train a simple model for demonstration
        self.model = RandomForestClassifier(n_estimators=10, random_state=42)
        
        # Sample training data (synthetic for demo)
        # In production, use real clinical data
        self.X_train = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # No symptoms
            [1, 1, 1, 1, 1, 1, 1, 1, 0],  # Mild symptoms
            [2, 2, 2, 2, 1, 1, 2, 2, 1],  # Moderate symptoms
            [3, 3, 3, 3, 3, 3, 3, 3, 2],  # Severe symptoms
            [0, 1, 0, 1, 0, 1, 0, 1, 0],  # Mild variation
            [2, 2, 2, 2, 2, 2, 2, 2, 2],  # Moderate consistent
        ])
        self.y_train = np.array([0, 1, 2, 3, 1, 2])  # 0=None, 1=Mild, 2=Moderate, 3=Severe
        
        # Train model
        self.model.fit(self.X_train, self.y_train)
    
    def classify_score(self, phq9_score):
        """
        Classify depression severity based on PHQ-9 score
        
        Standard PHQ-9 interpretation:
        0-4: No depression
        5-9: Mild depression
        10-14: Moderate depression
        15-19: Moderately severe depression
        20-27: Severe depression
        """
        
        if phq9_score <= 4:
            return {
                'severity': 'None',
                'level': 0,
                'recommendation': 'No depression detected. Keep maintaining healthy habits.',
                'color': '✅'
            }
        elif phq9_score <= 9:
            return {
                'severity': 'Mild',
                'level': 1,
                'recommendation': 'Mild depression detected. Consider regular exercise, good sleep, and social connection.',
                'color': '🟡'
            }
        elif phq9_score <= 14:
            return {
                'severity': 'Moderate',
                'level': 2,
                'recommendation': 'Moderate depression detected. Professional counseling is recommended.',
                'color': '🟠'
            }
        elif phq9_score <= 19:
            return {
                'severity': 'Moderately Severe',
                'level': 3,
                'recommendation': 'Moderately severe depression detected. Please seek professional help.',
                'color': '🔴'
            }
        else:
            return {
                'severity': 'Severe',
                'level': 4,
                'recommendation': 'Severe depression detected. Please contact a mental health professional immediately.',
                'color': '🚨'
            }
    
    def get_therapeutic_response(self, severity_data):
        """Generate empathetic response based on severity"""
        
        responses = {
            'None': [
                "That's wonderful! It sounds like you're doing well mentally. Keep up these positive habits! 😊",
                "Your responses suggest good mental health. Continue what you're doing!"
            ],
            'Mild': [
                "I notice some mild symptoms. Remember, it's normal to feel down sometimes. Here are some tips:\n• Get 7-8 hours of sleep\n• Exercise 30 minutes daily\n• Spend time with loved ones\n• Practice mindfulness",
                "You're experiencing some mild symptoms. These are common, and many people overcome them with self-care."
            ],
            'Moderate': [
                "Your responses suggest moderate depression. I strongly encourage you to:\n• Talk to a counselor or therapist\n• Visit your doctor\n• Maintain routine\n• Reach out to friends/family\n\nYou don't have to face this alone.",
                "I'm concerned about what you've shared. Professional support can make a real difference. Would you like resources?"
            ],
            'Moderately Severe': [
                "Your symptoms seem quite significant. Please reach out to a mental health professional:\n🏥 National Helpline: 1-800-XXX-XXXX\n💬 Crisis Chat: www.crisis.org\nYou deserve professional support.",
                "I care about your wellbeing. Please don't hesitate to contact a professional therapist or counselor."
            ],
            'Severe': [
                "⚠️ URGENT: Your responses indicate severe depression. PLEASE reach out immediately:\n🚨 Crisis Line: Call 911 or 988 (Suicide & Crisis Lifeline)\n💬 Text HOME to 741741\nYour life has value. Help is available NOW.",
                "Your wellbeing is important. Please contact emergency services or a crisis line immediately."
            ]
        }
        
        return responses.get(severity_data['severity'], ["Let's continue our conversation."])
    
    def calculate_phq9_score(self, answers):
        """
        Calculate total PHQ-9 score from answers
        answers: list of integers [0-3] for each question
        """
        if not answers or len(answers) != 9:
            return None
        
        total_score = sum(answers)
        return total_score

if __name__ == "__main__":
    detector = DepressionDetector()
    
    # Test examples
    test_scores = [2, 7, 12, 17, 23]
    
    for score in test_scores:
        result = detector.classify_score(score)
        print(f"\nPHQ-9 Score: {score}")
        print(f"Severity: {result['severity']}")
        print(f"Recommendation: {result['recommendation']}")
