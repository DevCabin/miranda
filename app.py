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
from flask import Flask, request, jsonify

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

@app.route('/api/query', methods=['POST'])
def query():
    try:
        # Get sheet data
        result = sheets.spreadsheets().values().get(
            spreadsheetId=os.environ.get('GOOGLE_SHEETS_SPREADSHEET_ID'),
            range='A1:Z'
        ).execute()
        data = result.get('values', [])

        # Query Gemini
        prompt = f"""
        Analyze this spreadsheet data: {data}
        User question: {request.json.get('query', '')}
        """
        response = model.generate_content(prompt)
        
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(port=3000) 