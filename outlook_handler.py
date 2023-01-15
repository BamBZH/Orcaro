from operator import attrgetter

from O365 import Account, MSGraphProtocol
import datetime as dt
import calendar as cal
from utils import prtInfo, prtError, prtWarning, prtResult, parse_date

# IDs we get from Azure account
CLIENT_ID = '0c99ed1d-1787-4d35-8a59-6ad691fd2b07'
SECRET_ID = 'pGo8Q~IAJtpL2VMWJKAhuyFE2HL9j7oN0rs.gbl6'




class OutlookHandler:
    credentials = (CLIENT_ID, SECRET_ID)

    def __init__(self):
        protocol = MSGraphProtocol()
        self.scopes = ['calendar', 'calendar_shared']
        self.account = Account(self.credentials, protocol=protocol)
        self.events = []

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

