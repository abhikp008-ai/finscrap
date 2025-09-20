"""
Configuration for Google Sheets integration
"""
import os
import json
from django.conf import settings

# Google Sheets configuration
SPREADSHEET_NAME = "Financial News Scraper Data"
CONFIG_FILE = "sheets_config.json"

# Google OAuth 2.0 Credentials - Load from environment variables
def get_google_oauth_credentials():
    """Get Google OAuth credentials from environment variables"""
    client_id = os.environ.get('GOOGLE_OAUTH_CLIENT_ID')
    client_secret = os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        raise ValueError(
            "Google OAuth credentials not found. Please set environment variables:\n"
            "GOOGLE_OAUTH_CLIENT_ID=your_client_id\n"
            "GOOGLE_OAUTH_CLIENT_SECRET=your_client_secret"
        )
    
    return {
        "web": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "redirect_uris": [
                "https://finscrap-production.up.railway.app"
            ]
        }
    }

# For backward compatibility, try to get credentials
try:
    GOOGLE_OAUTH_CREDENTIALS = get_google_oauth_credentials()
except ValueError:
    # Fallback to None if credentials not available
    GOOGLE_OAUTH_CREDENTIALS = None

def get_or_create_spreadsheet_id():
    """Get existing spreadsheet ID from config file or environment"""
    # First check environment variable
    spreadsheet_id = os.environ.get('FINANCIAL_NEWS_SPREADSHEET_ID')
    if spreadsheet_id:
        return spreadsheet_id
    
    # Then check config file
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                return config.get('spreadsheet_id')
    except Exception:
        pass
    
    return None

def save_spreadsheet_id(spreadsheet_id):
    """Save spreadsheet ID to config file"""
    try:
        config = {}
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
        
        config['spreadsheet_id'] = spreadsheet_id
        
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
        
        # Also set in environment for current process
        os.environ['FINANCIAL_NEWS_SPREADSHEET_ID'] = spreadsheet_id
    except Exception as e:
        print(f"Warning: Could not save spreadsheet ID to config: {e}")