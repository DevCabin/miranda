# Miranda v1.0.0 - Gemini + Sheets Integration

A serverless API that connects Google's Gemini AI with Google Sheets data. Ask questions about your spreadsheet data in natural language.

## Live Demo
https://miranda-eight.vercel.app/

## API Endpoints

### Health Check
```bash
curl https://miranda-eight.vercel.app/api/health
```

### Query Spreadsheet
```bash
curl -X POST https://miranda-eight.vercel.app/api/query \
-H "Content-Type: application/json" \
-d '{"query": "What data do you see in the spreadsheet?"}'
```

## Deployment

### 1. Fork or Clone Repository
Fork this repository to your GitHub account

### 2. Connect to Vercel
- Go to [Vercel](https://vercel.com)
- Create New Project
- Import your forked repository
- Select Python framework preset

### 3. Configure Environment Variables
In Vercel project settings, add:
```env
GEMINI_API_KEY=your_gemini_api_key
GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id
GOOGLE_SHEETS_SERVICE_ACCOUNT_FILE_CONTENT={"type":"service_account",...}
```

### 4. Deploy
Vercel will automatically deploy when you push changes to your repository.

## Example Queries
- "What data do you see in the spreadsheet?"
- "Give me a brief summary of the main themes"
- "What are the recommendations about time management?"

## Architecture
- Vercel serverless deployment
- Flask API endpoints
- Gemini Pro model for AI processing
- Google Sheets API for data access
- JSON response format

## Stable Version
This is tagged as v1.0.0. To revert to this stable version:
1. Go to your Vercel project
2. Go to Deployments
3. Find the deployment tagged with v1.0.0
4. Click "..." and select "Promote to Production"

## Security Notes
- Never commit credentials to repository
- Use Vercel's environment variables exclusively
- Regenerate API keys if accidentally exposed
- Keep service account credentials secure

## Status
✅ Production: Working and stable 