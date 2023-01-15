import calendar
import datetime as dt
from typing import Tuple

from colorama import Fore, Style


def prtWarning(message):
    # arg2 = ('\033[1;93m') + args + ('\033[0;37m')
    # arg = Fore.LIGHTBLACK_EX + args
    # __builtin__.print(*arg2, **kwargs)
    print(Fore.LIGHTBLACK_EX + message + Style.RESET_ALL)


def prtInfo(message):
    # arg2 = ('\033[0;94m',) + args + ('\033[0;37m',)
    # arg2 = Fore.LIGHTBLUE_EX + args
    # __builtin__.print(*arg2, **kwargs)
    print(Fore.LIGHTBLUE_EX + message + Style.RESET_ALL)


def prtResult(message):
    # arg2 = ('\033[0;92m',) + args + ('\033[0;37m',)
    # arg2 = Fore.GREEN + args
    # __builtin__.print(*arg2, **kwargs)
    print(Fore.GREEN + message + Style.RESET_ALL)


def prtError(message):
    # arg2 = ('\033[1;91m',) + args + ('\033[0;37m',)
    # arg2 = Fore.RED + args
    # __builtin__.print(*arg2, **kwargs)
    print(Fore.RED + message + Style.RESET_ALL)


def parse_date(date) -> Tuple:
    date_list = date.split('/')
    if len(date_list) == 3:
        date_fmt = dt.datetime.strptime(date, '%d/%m/%y')
        start_date = dt.datetime(date_fmt.year, date_fmt.month, date_fmt.day)
        end_date = start_date + dt.timedelta(days=6)
    # date formatted as mm/yy
    elif len(date_list) == 2:
        date_fmt = dt.datetime.strptime("01/" + date, '%d/%m/%y')
        month_range = calendar.monthrange(date_fmt.year, date_fmt.month)
        start_date = dt.datetime(date_fmt.year, date_fmt.month, date_fmt.day)
        end_date = dt.datetime(date_fmt.year, date_fmt.month, month_range[1])

    return start_date, end_date


def increment_date(date: str, idx: int) -> str:
    date += dt.timedelta(days=idx)
    return date.strftime("%d/%m/%y")
