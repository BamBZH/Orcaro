import warnings
from cmd import Cmd

from colorama import Fore, Style, init
from oauthlib.oauth2 import TokenExpiredError

from data_model import DataModel
from excel_handler import ExcelHandler
from outlook_handler import OutlookHandler
from utils import prtWarning

warnings.filterwarnings('ignore')
init(convert=True)

class OrcaroCmdLineApp(Cmd):

    def __init__(self):
        super().__init__()
        self.intro = Fore.LIGHTBLUE_EX + "\nBienvenue sur Orcaro ! L'outil d'organisation de Caro BdG la meuf la plus badass in the world !\n" + Style.RESET_ALL + \
                     "Type help to see the list of commands you can execute"
        self.prompt = 'orcaro> '
        self.tracestatus = True

    def preloop(self):
        """Initialize Outlook module"""
        self.outlook = OutlookHandler()

    def emptyline(self):
        # do nothing but prevents Cmd to run last command
        return False

    def precmd(self, line):
        # for debug purpose
        return line

    def do_trace(self, arg):
        """Set trace status (on|off)"""
        if arg == 'on':
            self.tracestatus = True
        elif arg == 'off':
            self.tracestatus = False

    def do_events(self, arg):
        """ returns the list of event for week starting with the first argument 'date'
        Ex :
        > events 01/01/1970
        > events
        """

        try:
            # Fetch events
            events = self.outlook.fetch_events(arg)
            # Compute the ratio per mission
            self.data_model = DataModel(events)
            self.data_model.sort_events()
            self.data_model.show_events()
            self.data_model.compute_time_spent()
            self.data_model.compute_ratios()
            self.data_model.show_time_per_mission()
            self.data_model.show_ratio_per_mission()
            excel_handler = ExcelHandler(self.data_model.ratio_per_mission, arg)
            excel_handler.create_excel_file()
        except TokenExpiredError:
            prtWarning("Token expired. Please call authenticate method.")

    def do_authenticate(self, arg):
        self.outlook.authenticate()


app = OrcaroCmdLineApp()
app.cmdloop()
