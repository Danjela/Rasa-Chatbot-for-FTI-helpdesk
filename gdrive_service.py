import logging

import gspread
import tempfile
from oauth2client.service_account import ServiceAccountCredentials
from gspread.models import Spreadsheet
from typing import List, Text, Optional

import os

logger = logging.getLogger(__name__)


class GDriveService:
    """Service to write to a spread sheet in google drive."""

    # Name of the spreadsheet
    SPREADSHEET_NAME = "Lista e kërkesave për dokumenta"

    # Sheet where the new address change entries should be stored in
    SHEET_NAME = "FTI"

    def __init__(self, gdrive_credentials_json: Text = os.environ.get("GDRIVE_CREDENTIALS", "")):

        scopes = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file"
        ]

        # authenticate the service with a json key
        
        self.creds= ServiceAccountCredentials.from_json_keyfile_name("credentials.json",scopes)

    def request_sheet(self, sheet_name: Text) -> Optional[Spreadsheet]:
        # fetch a specific sheet
        logging.debug("Refreshing auth")
        try:
            return gspread.authorize(self.creds).open(sheet_name)
        except Exception as e:
            logging.error(
                "Failed to create google spreadsheet connection. %s", e, exc_info=True
            )
            return None

    def store_data(self, data: List[Text]) -> None:
        """Adds a single new row to the sheet containing the user's
        information"""
        self.append_row(self.SPREADSHEET_NAME, data, self.SHEET_NAME)

    def store_comments(self, data: List[Text]) -> None:
        """Adds a single new row to the sheet containing the user's
        comments"""
        self.append_row(self.SPREADSHEET_NAME, data, "Komente")

    def append_row(
        self, sheet_name: Text, row_values: List[Text], worksheet_name: Text
    ) -> None:
        # add a row to the spreadsheet
        sheet = self.request_sheet(sheet_name)
        if sheet:
            try:
                worksheet = sheet.worksheet(worksheet_name)
                if worksheet:
                    worksheet.append_row(row_values)
            except Exception as e:
                logging.error(
                    f"Failed to write row to gdocs. Sheet {sheet_name}/{worksheet_name}. "
                    f"Error: {e}",
                    exc_info=True,
                )