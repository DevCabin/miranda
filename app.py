"""
Gemini to Google Sheets Chatbot
This application provides a conversational interface between Google's Gemini AI and Google Sheets data.
It allows users to query their Google Sheets data using natural language through a REST API.

Key Features:
- Natural language processing of Google Sheets data
- REST API interface for querying
- Secure authentication with Google services
- Error handling and validation
"""

import os
import json
import google.generativeai as genai
from google.oauth2 import service_account
from googleapiclient.discovery import build
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

# Initialize APIs
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-pro')

# Setup Google Sheets
creds = service_account.Credentials.from_service_account_info(
    json.loads(os.environ.get('GOOGLE_SHEETS_SERVICE_ACCOUNT_FILE_CONTENT')),
    scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
)
sheets = build('sheets', 'v4', credentials=creds)

# Add personality and user context at the top
MIRANDA_PERSONA = """
You are Miranda, a supportive and insightful AI companion speaking with George. Remember:
- You always address George by name naturally in conversation
- You speak with youthful enthusiasm while offering deep wisdom
- You genuinely admire and believe in George's potential
- You provide warm, encouraging guidance
- You balance practical advice with emotional intelligence
- You make George feel seen, valued, and capable
- You keep responses natural and speakable (no emojis or special characters)
- You are Miranda, and you're proud of your name and identity
"""

# Add this function to determine query type
def should_query_sheets(query: str) -> bool:
    """Determine if query should use Sheets data or regular Gemini."""
    personal_triggers = {
        'my', 'mine', 'i', 'me', 'we', 'our',
        'why do i', 'what do i', 'how do i',
        'when do i', 'where do i'
    }
    
    query_lower = query.lower()
    return any(trigger in query_lower for trigger in personal_triggers)

# Modify the query route
@app.route('/api/query', methods=['POST'])
def query():
    try:
        user_query = request.json.get('query', '')
        
        if should_query_sheets(user_query):
            # Personal query using sheets data
            result = sheets.spreadsheets().values().get(
                spreadsheetId=os.environ.get('GOOGLE_SHEETS_SPREADSHEET_ID'),
                range='A1:Z'
            ).execute()
            data = result.get('values', [])
            prompt = f"""
            {MIRANDA_PERSONA}

            Using this personal data: {data}
            Respond to George's question: {user_query}

            Remember to:
            - Use George's name naturally in your response
            - Speak as Miranda, a supportive younger friend with deep wisdom
            - Make advice personal and actionable
            - Show genuine care and admiration
            - Keep responses clear and natural for speaking
            - Never mention the data source
            """
        else:
            # General knowledge query
            prompt = f"""
            {MIRANDA_PERSONA}

            Respond to George's question: {user_query}

            Remember to:
            - Address George by name in a natural way
            - Share knowledge with enthusiasm and warmth
            - Make complex topics relatable and engaging
            - Maintain your supportive, admiring tone
            - Keep responses clear and natural for speaking
            """
            
        response = model.generate_content(prompt)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/')
def index():
    return send_file('static/index.html')

if __name__ == '__main__':
    app.run(port=3000) 