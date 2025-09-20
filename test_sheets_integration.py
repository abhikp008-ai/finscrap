#!/usr/bin/env python3
"""
Simple test script to verify Google Sheets integration
Run this to test if the enhanced functionality works correctly
"""

import os
import sys

# Add the project directory to the path
sys.path.insert(0, '/Users/abhishek/Documents/FinScrapeDashboard')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finscrap.settings')

import django
django.setup()

from newscraper.google_sheets_service import GoogleSheetsService
from newscraper.sheets_config import create_or_get_spreadsheet, SPREADSHEET_NAME

def test_spreadsheet_functionality():
    """Test the enhanced spreadsheet functionality"""
    
    print("Testing Google Sheets Integration...")
    print("=" * 50)
    
    try:
        # Test 1: Initialize service
        print("1. Initializing Google Sheets service...")
        sheets_service = GoogleSheetsService()
        print("   ✓ Service initialized successfully")
        
        # Test 2: Create or get spreadsheet
        print("2. Creating or getting spreadsheet...")
        test_name = "FinScrap Test Spreadsheet"
        spreadsheet_id = create_or_get_spreadsheet(test_name)
        
        if spreadsheet_id:
            print(f"   ✓ Spreadsheet ID: {spreadsheet_id}")
            print(f"   ✓ URL: {sheets_service.get_sheet_url(spreadsheet_id)}")
        else:
            print("   ✗ Failed to create/get spreadsheet")
            return False
        
        # Test 3: Test finding by name
        print("3. Testing find by name functionality...")
        found_id = sheets_service.find_spreadsheet_by_name(test_name)
        if found_id == spreadsheet_id:
            print("   ✓ Successfully found spreadsheet by name")
        else:
            print("   ✗ Failed to find spreadsheet by name")
        
        # Test 4: Test data insertion
        print("4. Testing data insertion...")
        test_data = [
            {
                'title': 'Test Article 1',
                'url': 'https://example.com/test1',
                'date': '2024-01-01',
                'content': 'This is test content for article 1',
                'source': 'test'
            },
            {
                'title': 'Test Article 2', 
                'url': 'https://example.com/test2',
                'date': '2024-01-02',
                'content': 'This is test content for article 2',
                'source': 'test'
            }
        ]
        
        rows_added = sheets_service.store_news_data(spreadsheet_id, test_data, 'TestSource')
        print(f"   ✓ Added {rows_added} rows to spreadsheet")
        
        # Test 5: Test data reading
        print("5. Testing data reading...")
        all_data = sheets_service.get_all_news_data(spreadsheet_id)
        print(f"   ✓ Read {len(all_data)} articles from spreadsheet")
        
        # Test 6: Test deduplication
        print("6. Testing deduplication...")
        duplicate_rows = sheets_service.store_news_data(spreadsheet_id, test_data, 'TestSource')
        print(f"   ✓ Duplicate insertion prevented: {duplicate_rows} rows added (should be 0)")
        
        print("\n" + "=" * 50)
        print("🎉 All tests passed! The enhanced Google Sheets integration is working correctly.")
        print(f"\nView your test spreadsheet at: {sheets_service.get_sheet_url(spreadsheet_id)}")
        
        return True
        
    except Exception as e:
        print(f"   ✗ Error: {e}")
        print("\n" + "=" * 50)
        print("❌ Tests failed. Please check your configuration and authentication.")
        return False

if __name__ == "__main__":
    test_spreadsheet_functionality()