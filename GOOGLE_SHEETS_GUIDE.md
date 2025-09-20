# Google Sheets Integration Usage Guide

## Overview
The FinScrapeDashboard now includes enhanced Google Sheets integration that allows you to:

1. Create a spreadsheet with a given name
2. Check if a spreadsheet already exists before creating a new one
3. Insert scraped data into the spreadsheet from different sources
4. Read the spreadsheet data and display it on the dashboard

## Setup

### 1. Google API Credentials
Set up your environment variables for Google OAuth:
```bash
export GOOGLE_OAUTH_CLIENT_ID="your_client_id"
export GOOGLE_OAUTH_CLIENT_SECRET="your_client_secret"
```

### 2. Authentication
Run the authentication setup command:
```bash
python manage.py setup_google_auth
```

## Usage

### 1. Create or Get a Spreadsheet
You can create a new spreadsheet or get an existing one by name:

```bash
# Use default name ("Financial News Scraper Data")
python manage.py create_spreadsheet

# Use custom name
python manage.py create_spreadsheet --name "My Custom Financial Data"
```

This command will:
- Check if a spreadsheet with the given name already exists in your Google Drive
- If it exists, it will use that spreadsheet
- If it doesn't exist, it will create a new one
- Save the spreadsheet ID for future use

### 2. Run Scrapers
The scrapers will automatically use the configured spreadsheet:

```bash
# Scrape from specific source
python manage.py scrape_moneycontrol --max-pages 5
python manage.py scrape_financialexpress --max-pages 3
python manage.py scrape_livemint --max-pages 2

# Scrape from all sources
python manage.py scrape_all --max-pages 3
```

### 3. View Data on Dashboard
Access the web dashboard to:
- View scraped articles with pagination
- Filter by source, date range, or search terms
- Download data as CSV
- Access the Google Spreadsheet directly via the provided link

### 4. Direct Google Sheets Access
The dashboard shows a direct link to your Google Spreadsheet where you can:
- View all scraped data
- Organize data by source (each source gets its own sheet)
- Perform advanced analysis using Google Sheets features

## Features

### Automatic Spreadsheet Management
- **Name-based lookup**: Finds existing spreadsheets by name to avoid duplicates
- **Auto-creation**: Creates spreadsheets only when needed
- **ID persistence**: Saves spreadsheet IDs for efficient reuse

### Data Organization
- **Source separation**: Each news source gets its own sheet
- **Deduplication**: Prevents duplicate articles based on URL
- **Timestamping**: Tracks when articles were scraped

### Dashboard Integration
- **Real-time sync**: Dashboard reads directly from Google Sheets
- **Filtering**: Filter articles by source, date, or search terms
- **Export options**: Download filtered data as CSV
- **Direct access**: Quick link to view data in Google Sheets

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_OAUTH_CLIENT_ID` | Google OAuth Client ID | Yes |
| `GOOGLE_OAUTH_CLIENT_SECRET` | Google OAuth Client Secret | Yes |
| `FINANCIAL_NEWS_SPREADSHEET_ID` | Specific spreadsheet ID to use | No |
| `GOOGLE_TOKEN_FILE` | Path to store auth tokens | No |

## Troubleshooting

### Authentication Issues
If you encounter authentication errors:
1. Verify your environment variables are set correctly
2. Re-run the authentication setup: `python manage.py setup_google_auth`
3. Check that your Google Cloud project has the necessary APIs enabled

### Spreadsheet Not Found
If the system can't find your spreadsheet:
1. Run `python manage.py create_spreadsheet --name "Your Spreadsheet Name"`
2. Check that the spreadsheet exists in your Google Drive
3. Verify you have the correct permissions

### Data Not Appearing
If scraped data doesn't appear:
1. Check the scraper logs for errors
2. Verify the spreadsheet ID is saved correctly
3. Refresh the dashboard page
4. Check the Google Spreadsheet directly for recent data

## API Permissions Required

Ensure your Google Cloud project has these APIs enabled:
- Google Sheets API
- Google Drive API

And the OAuth application has these scopes:
- `https://www.googleapis.com/auth/spreadsheets`
- `https://www.googleapis.com/auth/drive.file`