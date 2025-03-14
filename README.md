# Gemini to Google Sheets Chatbot

A conversational interface that connects Google's Gemini AI with Google Sheets data. This chatbot allows you to query your Google Sheets data using natural language.

## Prerequisites

- Python 3.8 or higher
- Google Cloud Project with Gemini API enabled
- Google Sheets API enabled
- Service account with access to Google Sheets

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with the following variables:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   GOOGLE_SHEETS_SERVICE_ACCOUNT_FILE_CONTENT=your_service_account_json_content
   GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id
   ```

   Note: For the `GOOGLE_SHEETS_SERVICE_ACCOUNT_FILE_CONTENT`, you need to copy the entire contents of your service account JSON file as a string.

## Usage

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. The server will start on port 8080 (or the port specified in your environment variables)

3. Send POST requests to `/query` endpoint with your questions:
   ```bash
   curl -X POST http://localhost:8080/query \
     -H "Content-Type: application/json" \
     -d '{"query": "What is the total sales in Sheet1?"}'
   ```

4. Check the health of the service:
   ```bash
   curl http://localhost:8080/health
   ```

## Example Queries

- "What is the total sales in Sheet1?"
- "Show me the data from Sheet1!A1:B10"
- "What is the average value in column B?"

## Error Handling

The application includes comprehensive error handling for:
- Missing environment variables
- Google Sheets API errors
- Invalid queries
- Server errors

## Future Enhancements

- Voice chat interface
- More sophisticated data analysis capabilities
- Support for writing to Google Sheets
- Enhanced natural language processing 