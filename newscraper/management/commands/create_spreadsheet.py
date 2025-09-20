from django.core.management.base import BaseCommand
import logging
from newscraper.google_sheets_service import GoogleSheetsService
from newscraper.sheets_config import save_spreadsheet_id, SPREADSHEET_NAME

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Create or get a Google Spreadsheet by name'

    def add_arguments(self, parser):
        parser.add_argument(
            '--name',
            type=str,
            default=SPREADSHEET_NAME,
            help='Name of the spreadsheet to create or get',
        )

    def handle(self, *args, **options):
        spreadsheet_name = options['name']
        
        try:
            # Initialize Google Sheets service
            sheets_service = GoogleSheetsService()
            
            # First check if a spreadsheet with this name already exists
            existing_id = sheets_service.find_spreadsheet_by_name(spreadsheet_name)
            
            if existing_id:
                # Spreadsheet already exists
                save_spreadsheet_id(existing_id)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Found existing spreadsheet "{spreadsheet_name}" with ID: {existing_id}'
                    )
                )
                self.stdout.write(f'URL: {sheets_service.get_sheet_url(existing_id)}')
            else:
                # Create new spreadsheet
                spreadsheet_id = sheets_service.create_spreadsheet(spreadsheet_name)
                save_spreadsheet_id(spreadsheet_id)
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created new spreadsheet "{spreadsheet_name}" with ID: {spreadsheet_id}'
                    )
                )
                self.stdout.write(f'URL: {sheets_service.get_sheet_url(spreadsheet_id)}')
            
        except Exception as e:
            logger.error(f'Failed to create/get spreadsheet: {e}')
            self.stdout.write(
                self.style.ERROR(f'Failed to create/get spreadsheet: {e}')
            )