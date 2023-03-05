import configparser
import datetime as dt
from typing import Tuple

from O365 import Account, MSGraphProtocol

from utils import prtInfo, prtError, prtResult, parse_date

class OutlookHandler:

    def __init__(self):
        protocol = MSGraphProtocol()
        self.scopes = ['calendar', 'calendar_shared']
        self.credentials = self.load_config()
        self.account = Account(self.credentials, protocol=protocol)
        self.events = []
    def load_config(self) -> Tuple:
        config = configparser.ConfigParser()
        config.read('config.ini')

        try:
            client_id = config['AZURE']['ClientId']
            secret_id = config['AZURE']['SecretId']
        except KeyError:
            prtError('config.ini is not correct!')

        return client_id, secret_id
    def authenticate(self) -> bool:

        prtInfo("\nAuthenticating...")
        if self.account.authenticate(scopes=self.scopes):
            prtResult('Authenticated! :)')
            return True
        else:
            prtError('Authentication failed! :(')
            return False

    def fetch_events(self, date):
        """
        :returns: a list of events
        * for the week starting with the first argument 'date' formatted as 01/01/23 for the 1st january of 2023
        * for the month if 'date' formatted as january, february...
        """

        prtInfo("\nFetching events...")

        schedule = self.account.schedule()
        calendar = schedule.get_default_calendar()

        # Build query to get events from date
        # date formatted as dd/mm/yy
        start_date, end_date = parse_date(date)

        query = calendar.new_query('start').greater_equal(start_date)
        query.chain('and').on_attribute('end').less_equal(end_date)

        # fetch the events
        events = calendar.get_events(query=query, include_recurring=False)

        self.events = events
        return events

    def get_duration(self, start: dt, end: dt) -> int:
        return end.hour - start.hour
