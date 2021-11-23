from csv import reader as csv_reader
from requests import get as get_csv


class Spreadsheet:
    def __init__(self, spreadsheet_id):
        self.data = []
        self.URL = f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv'
        self.fetch()

    def fetch(self):
        """
        Fetch a spreadsheet from Google Sheets
        """

        spreadsheet_csv = get_csv(self.URL).text

        # Here we parse the CSV
        reader = csv_reader(spreadsheet_csv.splitlines(), delimiter=',')

        # We return the iterator
        self.data = list(reader)[1:]

    def get(self):
        """
        Return the data as a list of rows.
        """

        return self.data

