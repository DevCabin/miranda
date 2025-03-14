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
from langchain.agents import AgentType, initialize_agent
from langchain.llms import GooglePalm
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from flask import Flask, request, jsonify
from typing import Optional

# Load environment variables from .env file
# This allows for secure configuration without hardcoding sensitive values
load_dotenv()

# ------------------ Configuration ------------------
# Retrieve and validate required environment variables
# These variables are essential for both Gemini AI and Google Sheets access
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GOOGLE_SHEETS_SERVICE_ACCOUNT_FILE_CONTENT = os.getenv("GOOGLE_SHEETS_SERVICE_ACCOUNT_FILE_CONTENT")
GOOGLE_SHEETS_SPREADSHEET_ID = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID")

# Validate that all required environment variables are present
# This prevents runtime errors due to missing configuration
if not all([GEMINI_API_KEY, GOOGLE_SHEETS_SERVICE_ACCOUNT_FILE_CONTENT, GOOGLE_SHEETS_SPREADSHEET_ID]):
    raise ValueError("Missing required environment variables. Please check your .env file.")

# Initialize Gemini AI with the provided API key
# This sets up the connection to Google's Gemini AI service
genai.configure(api_key=GEMINI_API_KEY)

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
        # Parse the service account JSON content from environment variables
        service_account_info = json.loads(GOOGLE_SHEETS_SERVICE_ACCOUNT_FILE_CONTENT)
        # Create credentials with read-only access to Google Sheets
        creds = service_account.Credentials.from_service_account_info(
            service_account_info,
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
        # Build and return the Google Sheets service
        return build('sheets', 'v4', credentials=creds)
    except Exception as e:
        raise Exception(f"Failed to initialize Google Sheets service: {str(e)}")

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

# ------------------ Tool Definition ------------------
def retrieve_sheet_data(sheet_name_and_range: str) -> str:
    """
    Retrieves data from a Google Sheet and formats it for the Langchain agent.
    
    This function is used as a tool by the Langchain agent to access Google Sheets data.
    It expects input in the format 'SheetName!Range' (e.g., 'Sales!A1:B10').
    
    Args:
        sheet_name_and_range (str): Combined sheet name and range in format 'SheetName!Range'
    
    Returns:
        str: The data as a string, or an error message if retrieval fails
    """
    try:
        # Split the input into sheet name and range
        sheet_name, range_ = sheet_name_and_range.split("!")
        data = get_sheet_data(sheet_name, range_)
        if data:
            return str(data)
        return "No data found in the specified range."
    except Exception as e:
        return f"Error retrieving data: {str(e)}"

# ------------------ Langchain Setup ------------------
def create_agent():
    """
    Initialize and return the Langchain agent with Google Sheets access.
    
    This function:
    1. Creates a Google Palm LLM instance
    2. Defines the tools available to the agent
    3. Initializes the agent with the specified configuration
    
    Returns:
        A configured Langchain agent ready to process queries
    
    Raises:
        Exception: If there's an error creating the agent
    """
    try:
        # Initialize the language model with zero temperature for consistent results
        llm = GooglePalm(google_api_key=GEMINI_API_KEY, temperature=0)

        # Define the tools available to the agent
        tools = [
            Tool(
                name="google_sheet_retriever",
                func=retrieve_sheet_data,
                description="Retrieves data from Google Sheets. Input format: SHEET_NAME!RANGE (e.g., 'Sheet1!A1:B10')",
            )
        ]

        # Create and return the agent with the specified configuration
        return initialize_agent(
            tools,
            llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
        )
    except Exception as e:
        raise Exception(f"Failed to create agent: {str(e)}")

# Initialize the agent at startup
agent = create_agent()

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
        return agent.run(user_query)
    except Exception as e:
        return f"Error processing query: {str(e)}"

# ------------------ Flask App ------------------
app = Flask(__name__)

@app.route("/")
def home():
    """Root endpoint that returns basic API information."""
    return jsonify({
        "status": "running",
        "endpoints": {
            "query": "/api/query",
            "health": "/api/health"
        }
    })

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

# Export the Flask app for Vercel
app = app 