import requests

# curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=GEMINI_API_KEY" \
# -H 'Content-Type: application/json' \
# -X POST \
# -d '{
#   "contents": [{
#     "parts":[{"text": "Explain how AI works"}]
#     }]
#    }'


#read from .env file
from dotenv import load_dotenv
import os
import requests
import json

# Load environment variables
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

def ask_ai(question):
    """
    Send a question to Gemini AI and get response
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    data = {
        "contents": [{
            "parts": [{"text": question}]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise exception for bad status codes
        
        result = response.json()
        if 'candidates' in result:
            return result['candidates'][0]['content']['parts'][0]['text']
        return "Sorry, I couldn't process that request."
        
    except requests.exceptions.RequestException as e:
        return f"Error calling AI API: {str(e)}"