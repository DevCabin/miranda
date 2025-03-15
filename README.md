# Miranda - Voice AI Assistant with Google Sheets Integration

## Overview
Miranda is a personalized voice-enabled AI assistant that combines Google's Gemini AI with Google Sheets integration. She provides warm, insightful responses while maintaining access to your personal data through Google Sheets.

## Version 1.1.2 [STABLE]
Current stable release featuring:
- 🎙️ Continuous voice conversation with intelligent silence detection
- 🗣️ Fixed voice settings (Tessa at 0.9 speed) for optimal clarity
- 🔄 Smart pause/resume during conversations
- 📊 Google Sheets integration for personalized data access
- 🤖 Powered by Google's Gemini 1.5 Pro AI
- 💬 Consistent, warm personality as Miranda
- 🔒 Secure service account authentication

## Features
- **Intelligent Conversation**: Continuous voice interaction with 1-second silence detection
- **Natural Voice**: Optimized Tessa voice at 0.9 speed for perfect clarity
- **Visual Feedback**: Red/blue button states showing conversation status
- **Personal Context**: Maintains context and addresses you by name
- **Data Integration**: Securely accesses your Google Sheets data
- **Personality**: Warm, supportive responses with emotional intelligence
- **Flexible Queries**: Handles both personal (data-driven) and general knowledge questions

## Technical Requirements
- Python 3.8+
- Google Cloud Service Account
- Gemini API Key
- Google Sheets API enabled

## Environment Variables
Required environment variables in Vercel:
```env
GEMINI_API_KEY=your_gemini_api_key
GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id
GOOGLE_SHEETS_SERVICE_ACCOUNT_FILE_CONTENT={"type":"service_account",...}
```

## Live Demo
https://miranda-eight.vercel.app/

## Deployment
1. Fork this repository
2. Connect to Vercel and import the forked repository
3. Configure the environment variables above
4. Deploy - Vercel will automatically deploy from the main branch

## Example Queries
- "What data do you see in the spreadsheet?"
- "Give me a brief summary of the main themes"
- "What are the recommendations about time management?"

## Architecture
- Vercel serverless deployment
- Flask API endpoints
- Gemini Pro model for AI processing
- Google Sheets API for data access
- Web Speech API for voice interaction

## Security Notes
- Never commit credentials to repository
- Use Vercel's environment variables exclusively
- Regenerate API keys if accidentally exposed
- Keep service account credentials secure

## Status
✅ Production: Stable v1.1.2 with continuous conversation and fixed voice settings

## TODO
- Move persona configuration to separate config file
- Add conversation memory features
- Support for multiple data sources 