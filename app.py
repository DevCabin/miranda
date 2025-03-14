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
import google.generativeai as genai
from googleapiclient.discovery import build
from google.oauth2 import service_account
import json
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from typing import Optional

# Load environment variables from .env file
# This allows for secure configuration without hardcoding sensitive values
load_dotenv()

# Add this right after load_dotenv()
print("\n=== Environment Variable Debug ===")
content = os.getenv("GOOGLE_SHEETS_SERVICE_ACCOUNT_FILE_CONTENT")
print(f"First 20 chars: [{content[:20]}]")
print(f"Type: {type(content)}")

# ------------------ Configuration ------------------
# Retrieve and validate required environment variables
# These variables are essential for both Gemini AI and Google Sheets access
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GOOGLE_SHEETS_SERVICE_ACCOUNT_FILE_CONTENT = os.environ.get("GOOGLE_SHEETS_SERVICE_ACCOUNT_FILE_CONTENT")
GOOGLE_SHEETS_SPREADSHEET_ID = os.environ.get("GOOGLE_SHEETS_SPREADSHEET_ID")

# Validate that all required environment variables are present
# This prevents runtime errors due to missing configuration
if not all([GEMINI_API_KEY, GOOGLE_SHEETS_SERVICE_ACCOUNT_FILE_CONTENT, GOOGLE_SHEETS_SPREADSHEET_ID]):
    raise ValueError("Missing required environment variables")

# Initialize Gemini AI with the provided API key
# This sets up the connection to Google's Gemini AI service
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Modify fix_json_string to be more verbose
def fix_json_string(json_str):
    """Clean and validate JSON string from environment variable."""
    try:
        print("\n=== JSON Parsing Debug ===")
        print(f"Input string starts with: [{json_str[:20]}]")
        
        # Remove any outer quotes and whitespace
        cleaned = json_str.strip().strip('"').strip("'")
        print(f"After cleaning starts with: [{cleaned[:20]}]")
        
        # Try parsing
        result = json.loads(cleaned)
        print("JSON parsing successful!")
        return result
    except Exception as e:
        print(f"Error fixing JSON: {str(e)}")
        print(f"Error type: {type(e)}")
        raise

# ------------------ Google Sheets Setup ------------------
def get_sheets_service():
    """
    Initialize and return Google Sheets service.
    
    This function:
    1. Parses the service account credentials from environment variables
    2. Creates authentication credentials with read-only access to Google Sheets
    3. Builds and returns a Google Sheets service object
    
    Returns:
        A Google Sheets service object that can be used to interact with sheets
    
    Raises:
        Exception: If there's an error initializing the service
    """
    try:
        # Parse the service account info using our helper function
        service_account_info = json.loads(GOOGLE_SHEETS_SERVICE_ACCOUNT_FILE_CONTENT)
        
        # Create credentials
        creds = service_account.Credentials.from_service_account_info(
            service_account_info,
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
        return build('sheets', 'v4', credentials=creds)
    except Exception as e:
        print(f"Sheets service error: {str(e)}")
        raise

def get_sheet_data(sheet_name: str, range_: str) -> Optional[list]:
    """
    Retrieve data from specified Google Sheet range.
    
    Args:
        sheet_name (str): Name of the sheet to access
        range_ (str): The range to retrieve (e.g., 'A1:B10')
    
    Returns:
        Optional[list]: The data from the specified range, or None if empty
    
    Raises:
        Exception: If there's an error retrieving the data
    """
    try:
        service = get_sheets_service()
        sheet = service.spreadsheets()
        # Execute the API call to get the specified range
        result = sheet.values().get(
            spreadsheetId=GOOGLE_SHEETS_SPREADSHEET_ID,
            range=f"{sheet_name}!{range_}"
        ).execute()
        return result.get('values', [])
    except Exception as e:
        raise Exception(f"Failed to retrieve sheet data: {str(e)}")

# ------------------ Main Function ------------------
def query_gemini(user_query: str) -> str:
    """
    Process a user query using the Gemini agent.
    
    This function handles the interaction between the user's query and the Langchain agent,
    which in turn uses the Google Sheets tool to retrieve relevant data.
    
    Args:
        user_query (str): The natural language query from the user
    
    Returns:
        str: The agent's response to the query
    """
    try:
        # Get available sheets metadata
        service = get_sheets_service()
        sheet_metadata = service.spreadsheets().get(spreadsheetId=GOOGLE_SHEETS_SPREADSHEET_ID).execute()
        sheets = sheet_metadata.get('sheets', [])
        sheet_names = [sheet['properties']['title'] for sheet in sheets]
        
        # Get data from first sheet as sample
        sample_data = get_sheet_data(sheet_names[0], 'A1:Z10')  # Adjust range as needed
        
        # Construct context for Gemini
        context = f"""
        Available sheets: {', '.join(sheet_names)}
        Sample data from {sheet_names[0]}: {sample_data}
        
        User query: {user_query}
        
        Please analyze the data and respond to the query.
        """
        
        response = model.generate_content(context)
        return response.text
    except Exception as e:
        return f"Error processing query: {str(e)}"

# ------------------ Flask App ------------------
app = Flask(__name__)

@app.errorhandler(500)
def handle_500(e):
    return jsonify({
        "error": "Internal server error",
        "message": str(e)
    }), 500

@app.route("/")
def home():
    try:
        return jsonify({
            "status": "running",
            "endpoints": {
                "query": "/api/query",
                "health": "/api/health"
            }
        })
    except Exception as e:
        print(f"Error in home route: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/query", methods=["POST"])
def query():
    """
    Handle incoming queries via POST request.
    
    This endpoint:
    1. Validates the incoming request
    2. Processes the query using the Gemini agent
    3. Returns the response in JSON format
    
    Returns:
        JSON response containing either the query result or an error message
    """
    try:
        # Validate the request body
        data = request.get_json()
        if not data or "query" not in data:
            return jsonify({"error": "No query provided"}), 400
        
        # Process the query and return the response
        user_query = data["query"]
        response = query_gemini(user_query)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/health", methods=["GET"])
def health_check():
    """
    Health check endpoint for monitoring the service.
    
    This endpoint can be used by deployment platforms (like Vercel) to verify
    that the service is running properly.
    
    Returns:
        JSON response indicating the service status
    """
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    print("\n=== Testing API Components ===\n")
    
    # Test 1: Environment Variables
    print("1. Checking environment variables...")
    required_vars = ["GEMINI_API_KEY", "GOOGLE_SHEETS_SERVICE_ACCOUNT_FILE_CONTENT", "GOOGLE_SHEETS_SPREADSHEET_ID"]
    for var in required_vars:
        value = os.getenv(var)
        print(f"  {var}: {'✓ Set' if value else '✗ Missing'}")
    
    # Test 2: Google Sheets Connection
    print("\n2. Testing Google Sheets connection...")
    try:
        service = get_sheets_service()
        # Try to get the spreadsheet metadata
        sheet = service.spreadsheets().get(spreadsheetId=GOOGLE_SHEETS_SPREADSHEET_ID).execute()
        print(f"  ✓ Successfully connected to sheet: {sheet.get('properties', {}).get('title')}")
    except Exception as e:
        print(f"  ✗ Sheets connection failed: {str(e)}")
    
    # Test 3: Gemini API
    print("\n3. Testing Gemini API...")
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Say 'API test successful!'")
        print(f"  ✓ Gemini response: {response.text}")
    except Exception as e:
        print(f"  ✗ Gemini API failed: {str(e)}")
    
    # Test 4: Full Query Flow
    print("\n4. Testing complete query flow...")
    try:
        test_query = "What sheets are available?"
        response = query_gemini(test_query)
        print(f"  ✓ Query successful. Response: {response}")
    except Exception as e:
        print(f"  ✗ Query failed: {str(e)}")
    
    print("\n=== Test Complete ===\n")
    
    # Start the Flask app
    app.run(debug=True, port=3000, host='0.0.0.0')

print("\nService Account Content (first 150 chars):")
print(GOOGLE_SHEETS_SERVICE_ACCOUNT_FILE_CONTENT[:150]) 