from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from flask_session import Session
import requests
import json
import os
from datetime import datetime
import re

app = Flask(__name__)
CORS(app)

# Session configuration
app.config['SECRET_KEY'] = "YOUR SECRET CODE"
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)

# ========== ONLY UNHEALTH KEYWORDS (Non-Health Related) - ALL ENGLISH ==========
UNHEALTH_KEYWORDS = [
    'football', 'soccer', 'basketball', 'tennis', 'cricket', 'baseball', 'volleyball',
    'rugby', 'golf', 'hockey', 'boxing', 'wrestling', 'athletics', 'swimming',
    'sports', 'game', 'match', 'tournament', 'championship', 'league', 'cup',
    'team', 'player', 'coach', 'referee', 'stadium', 'goal', 'score', 'win', 'lose',
    'movie', 'film', 'cinema', 'hollywood', 'bollywood', 'actor', 'actress', 'director',
    'song', 'music', 'album', 'concert', 'festival', 'singer', 'musician', 'band',
    'entertainment', 'celebrity', 'famous', 'star', 'award', 'oscar', 'grammy',
    'politics', 'political', 'election', 'vote', 'voting', 'ballot', 'campaign',
    'president', 'prime minister', 'minister', 'government', 'parliament', 'congress',
    'senate', 'democrat', 'republican', 'party', 'policy', 'law', 'bill', 'act',
    'war', 'peace', 'army', 'military', 'navy', 'airforce', 'soldier', 'general',
    'weapon', 'gun', 'rifle', 'tank', 'missile', 'bomb', 'explosion', 'attack',
    'battle', 'fight', 'conflict', 'violence', 'terrorism', 'security',
    'money', 'dollar', 'euro', 'pound', 'yen', 'rupee', 'currency', 'cash', 'bank',
    'bitcoin', 'crypto', 'cryptocurrency', 'ethereum', 'dogecoin', 'blockchain',
    'stock', 'share', 'market', 'investment', 'trading', 'finance', 'financial',
    'price', 'cost', 'cheap', 'expensive', 'discount', 'sale', 'shopping', 'buy', 'sell',
    'weather', 'rain', 'sun', 'sunny', 'cloud', 'cloudy', 'snow', 'snowy', 'storm',
    'thunder', 'lightning', 'hurricane', 'typhoon', 'cyclone', 'tornado', 'flood',
    'drought', 'forecast', 'climate', 'temperature', 'degree', 'celsius', 'fahrenheit',
    'food', 'rice', 'pasta', 'pizza', 'burger', 'sandwich', 'salad', 'soup', 'bread',
    'meat', 'chicken', 'beef', 'fish', 'vegetable', 'fruit', 'apple', 'banana',
    'recipe', 'cook', 'cooking', 'chef', 'restaurant', 'cafe', 'kitchen', 'meal',
    'breakfast', 'lunch', 'dinner', 'snack', 'drink', 'water', 'juice', 'coffee', 'tea',
    'car', 'bus', 'train', 'plane', 'airplane', 'flight', 'airport', 'station',
    'taxi', 'uber', 'lyft', 'bike', 'bicycle', 'motorcycle', 'scooter', 'truck',
    'travel', 'vacation', 'holiday', 'tourist', 'tourism', 'hotel', 'resort', 'beach',
    'destination', 'trip', 'journey', 'cruise', 'ship', 'boat', 'ferry',
    'phone', 'smartphone', 'iphone', 'android', 'mobile', 'cellphone', 'tablet',
    'computer', 'laptop', 'desktop', 'mac', 'windows', 'linux', 'software', 'hardware',
    'app', 'application', 'website', 'web', 'internet', 'wifi', 'broadband', 'network',
    'gaming', 'console', 'playstation', 'xbox', 'nintendo', 'video game',
    'school', 'university', 'college', 'academy', 'institute', 'class', 'classroom',
    'student', 'teacher', 'professor', 'lecturer', 'homework', 'assignment', 'project',
    'exam', 'test', 'quiz', 'grade', 'score', 'degree', 'diploma', 'certificate',
    'subject', 'math', 'mathematics', 'physics', 'chemistry', 'biology', 'history',
    'geography', 'science', 'literature', 'english', 'language', 'art', 'music class',
    'work', 'job', 'career', 'profession', 'occupation', 'employment', 'unemployment',
    'salary', 'wage', 'income', 'pay', 'payment', 'bonus', 'benefit', 'insurance',
    'business', 'company', 'corporation', 'firm', 'enterprise', 'startup', 'office',
    'manager', 'employee', 'worker', 'staff', 'team', 'meeting', 'interview',
    'resume', 'cv', 'application', 'hire', 'recruitment', 'promotion', 'fire', 'quit',
    'shop', 'store', 'mall', 'market', 'supermarket', 'grocery', 'clothing', 'shoe',
    'fashion', 'style', 'brand', 'product', 'item', 'deal', 'offer', 'coupon',
    'news', 'newspaper', 'magazine', 'media', 'tv', 'television', 'channel', 'broadcast',
    'social media', 'facebook', 'twitter', 'instagram', 'tiktok', 'youtube', 'whatsapp',
    'fun', 'party', 'birthday', 'wedding', 'celebration', 'event', 'crypto', 'bitcoin'
]

# ========== GENERAL QUESTION PATTERNS (not health-specific) ==========
GENERAL_QUESTION_PATTERNS = [
    'what is', 'how to', 'how do', 'how does', 'how can', 'how could',
    'why is', 'why are', 'why do', 'why does', 'why did', 'why would',
    'tell me about', 'explain', 'explain me', 'what are', 'what was',
    'where is', 'where are', 'when is', 'when was', 'who is', 'who are'
]

# ========== SOMALI DETECTION ==========
SOMALI_WORDS = [
    'waxaan', 'waxaad', 'waxa', 'waxay', 'waxaa', 'waxaann',
    'kuwaas', 'kaas', 'taas', 'kuwa', 'kale', 'halka', 'halkan',
    'soomaali', 'somali', 'maalin', 'habeen', 'subax', 'galab', 'caawa',
    'fadlan', 'mahadsanid', 'salaam', 'calaykum', 'wacan', 'fiican',
    'xanuun', 'madax', 'qandho', 'qufac', 'calaamad', 'bukaan', 'dhakhtar',
    'aad', 'ah', 'ayaa', 'iyo', 'ugu', 'uun', 'dhex', 'socda', 'garaac', 'jaban'
]

def is_somali_language(text):
    """Check if the input text is in Somali language"""
    text_lower = text.lower().strip()
    
    for word in SOMALI_WORDS:
        if word in text_lower:
            return True
    
    somali_patterns = [
        r'waxaan qabaa', r'waxaan dareemayaa', r'waxaa igu', r'iga xanuunsanaysa',
        r'ma jiraan', r'sidee', r'goorma', r'halkee', r'ma ii sheegi', r'fadlan'
    ]
    for pattern in somali_patterns:
        if re.search(pattern, text_lower):
            return True
    
    return False

def is_health_related(text):
    """Check if the query is health-related - ONLY uses Unhealth keywords and Question patterns"""
    text_lower = text.lower().strip()
    
    # Check for general question patterns
    for pattern in GENERAL_QUESTION_PATTERNS:
        if pattern in text_lower:
            return False
    
    # Check for non-health keywords
    for word in UNHEALTH_KEYWORDS:
        if word in text_lower:
            return False
    
    # If no unhealthy patterns found, assume it's health-related
    return True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        symptoms = data.get('symptoms', '')
        age = data.get('age', '')
        sex = data.get('sex', '')
        duration = data.get('duration', '')
        severity = data.get('severity', '')
        
        if not symptoms or symptoms == '':
            return jsonify({'error': 'Please describe your symptoms'}), 400
        
        # ========== LANGUAGE VALIDATION: Check if input is Somali ==========
        if is_somali_language(symptoms):
            return jsonify({
                'result': """🔍 **Language Notice** 🔍

❌ **Fadlan Ingiriisi ku qor** (Please use English)

This health assistant responds in English only.

✅ **Please write your symptoms in English:**
• "I have a headache"
• "I feel fever and cough"
• "My stomach hurts"

💚 **Thank You**

---
*This AI health checker works best with English language input.*""",
                'disclaimer': '⚠️ Educational purposes only. Please use English for best results.'
            }), 200
        
        # ========== VALIDATION: Check if query is health-related ==========
        if not is_health_related(symptoms):
            return jsonify({
                'result': """🔍 **I'm a Health Assistant** 🔍

❌ **Sorry**, I can only help with health-related questions.

✅ **Please ask me about:**
• Your symptoms (headache, fever, cough, pain, etc.)
• Health conditions you're concerned about
• Wellness advice and home remedies
• When to consult a doctor

💚 Please ask health-related questions only.

*Sorry, I can only help with medical questions.*""",
                'disclaimer': '⚠️ Educational purposes only. Consult a healthcare professional.'
            }), 200
        
        prompt = f"""You are a highly qualified health advisor. Analyze this patient:
SYMPTOMS: {symptoms}
AGE: {age if age else 'Not specified'}
SEX: {sex if sex else 'Not specified'}
DURATION: {duration} days
SEVERITY: {severity}
Please respond in ENGLISH with this exact format:
🔍 POSSIBLE CONDITIONS (3 maximum):
• [Condition 1]
• [Condition 2]
• [Condition 3]
💊 HEALTH ADVICE & HOME REMEDIES:
• [Advice 1]
• [Advice 2]
• [Advice 3]
⚠️ WHEN TO CONSULT A DOCTOR:
• [Warning sign 1]
• [Warning sign 2]
• [Warning sign 3]
✅ PREVENTIVE MEASURES:
• [Measure 1]
• [Measure 2]
IMPORTANT: Educational purposes only. Consult a doctor for medical advice."""

        try:
            response = requests.post(
                'http://localhost:11434/api/generate',
                json={
                    'model': 'llama3.2:1b',
                    'prompt': prompt,
                    'stream': False,
                    'options': {
                        'temperature': 0.3,
                        'max_tokens': 800
                    }
                },
                timeout=90
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result.get('response', 'Unable to get response from AI')
            else:
                ai_response = get_fallback_advice(symptoms, severity)
                
        except Exception as e:
            print(f"Ollama error: {e}")
            ai_response = get_fallback_advice(symptoms, severity)
            
        return jsonify({
            'result': ai_response,
            'disclaimer': '⚠️ EDUCATIONAL PURPOSE ONLY. Please consult a healthcare professional.'
        })
        
    except requests.exceptions.Timeout:
        return jsonify({'error': 'AI response timeout. Please try again.'}), 500
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Ollama is not running! Please start Ollama first.'}), 500
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

def get_fallback_advice(symptoms, severity):
    """Fallback advice when AI is unavailable"""
    return """🔍 POSSIBLE CONDITIONS:
• Based on your symptoms, please consult a healthcare provider
💊 HEALTH ADVICE & HOME REMEDIES:
• Get adequate rest
• Stay hydrated
• Monitor your symptoms
⚠️ WHEN TO CONSULT A DOCTOR:
• Symptoms lasting more than 5-7 days
• Severe pain or discomfort
• High fever (above 103°F / 39.4°C)
✅ PREVENTIVE MEASURES:
• Maintain good hygiene
• Eat healthy foods
• Get regular check-ups"""

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)