# Miranda - Gemini to Google Sheets Chatbot

A serverless API that provides a conversational interface between Google's Gemini AI and Google Sheets data. This chatbot allows you to query your Google Sheets data using natural language through a REST API, deployed on Vercel.

## Overview

Miranda is designed to be a simple, serverless solution for querying Google Sheets data using natural language. It leverages Google's Gemini AI to understand user queries and process them against your Google Sheets data.

### Key Features
- Natural language processing of Google Sheets data
- Serverless deployment on Vercel
- REST API interface for querying
- Secure authentication with Google services
- Error handling and validation
- Health check endpoint for monitoring

## Prerequisites

1. Google Cloud Project with:
   - Gemini API enabled
   - Google Sheets API enabled
   - Service account with Sheets access
2. Vercel account
3. Git repository

## Environment Variables

The following environment variables must be set in your Vercel project:

```env
GEMINI_API_KEY=your_gemini_api_key
GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id
GOOGLE_SHEETS_SERVICE_ACCOUNT_FILE_CONTENT={"type":"service_account",...}
```

✅ **Verified**: All environment variables are currently set in Vercel project settings.

## Project Structure

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables in Vercel:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   GOOGLE_SHEETS_SERVICE_ACCOUNT_FILE_CONTENT=your_service_account_json_content
   GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id
   ```

   Note: For the `GOOGLE_SHEETS_SERVICE_ACCOUNT_FILE_CONTENT`, you need to copy the entire contents of your service account JSON file as a string.

## Deployment

This application is designed to be deployed exclusively on Vercel:

1. Push your code to a GitHub repository
2. Connect your repository to Vercel
3. Configure the environment variables in Vercel's project settings
4. Deploy!

The application will automatically deploy when you push changes to the main branch.

## API Endpoints

### Query Endpoint
```bash
POST /api/query
Content-Type: application/json

{
    "query": "What is the total sales in Sheet1?"
}
```

### Health Check
```bash
GET /api/health
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

## Development

This application is designed to be deployed directly to Vercel without local development. All changes should be made and tested through the Vercel deployment pipeline.

## Future Enhancements

- Voice chat interface
- More sophisticated data analysis capabilities
- Support for writing to Google Sheets
- Enhanced natural language processing
- Additional data source integrations

## License

MIT License - See LICENSE file for details

## Security Notes

- Never commit your `.env` file to version control
- Regenerate service account keys if they have been exposed
- Use environment variables in Vercel's dashboard instead of local `.env` files for production 