import os
import sys
import logging
import json
from datetime import datetime, timedelta


def get_base_path():
    try:
        if getattr(sys, "_MEIPASS", False):
            # base_path = os.path.abspath(os.path.join(sys._MEIPASS))
            base_path = os.path.abspath(getattr(sys, "_MEIPASS", ""))
        else:
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    except Exception as e:
        print(f"Error getting config path: {e}")

    print(f"Base path is = {base_path}")

    return base_path


def configure_logging():
    """Set up logging"""
    base_path = get_base_path()
    logs_dir = os.path.join(base_path, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    log_file = os.path.join(logs_dir, "data_matrix_logs.log")
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,  # (INFO, DEBUG, WARNING, ERROR, CRITICAL)
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def get_today_date():
    now = datetime.now()
    today_date = now.strftime("%d/%m/%Y")
    return today_date


def save_settings(**kwargs):
    """
    Args:
        **kwargs: Key-value pairs to update in the settings.json file.
    """
    logging.info("Save settings function triggered")
    config_file_path = os.path.join(get_base_path(), "config", "settings.json")
    logging.info(f"Settings.json path is = {config_file_path}")

    try:
        if os.path.exists(config_file_path):
            with open(config_file_path, "r") as f:
                current_settings = json.load(f)
        else:
            current_settings = {}

        current_settings.update(kwargs)

        with open(config_file_path, "w") as f:
            json.dump(current_settings, f, indent=4)

        logging.info("Settings JSON file updated successfully")

    except Exception as e:
        logging.error(f"Error saving settings: {e}")


def read_setting(key):

    logging.info("Read setting function triggered")
    config_file_path = os.path.join(get_base_path(), "config", "settings.json")
    logging.info(f"Settings.json path is = {config_file_path}")

    try:
        if os.path.exists(config_file_path):
            with open(config_file_path, "r") as f:
                settings = json.load(f)
            return settings.get(key)
        else:
            logging.warning("Settings.json file does not exist.")
            return ""
    except Exception as e:
        logging.error(f"Error reading settings: {e}")
        return ""

def get_icon_path():
    return os.path.join(get_base_path(), "assets", "icons","icon.ico")

def check_file_accessibility(file_path):
    try:
        if not os.path.exists(file_path):
            return False, "File does not exist."
        with open(file_path, 'a'):
            pass
        return True, "File is accessible."
    except PermissionError:
        return False, "Permission denied.File is already open in another application."



def is_time_valid_for_daily_report():
    now = datetime.now()

    # 3:40 PM today
    start_time = now.replace(hour=15, minute=40, second=0, microsecond=0)

    # 9:30 AM the next day
    end_time = (start_time + timedelta(days=1)).replace(hour=9, minute=30, second=0, microsecond=0)

    if start_time <= now < end_time:
        return True
    return False

def check_daily_report_validations():

    if get_today_date() != read_setting("last_fetch_data_date"):
        logging.error(f"User tried to generate daily reports without Fetching data")
        return False, "Please Fetch and Update data first and try again"

    if read_setting("last_daily_report_date") == get_today_date():
        logging.error(f"User tried to generate daily reports twice.")
        return False , "You have already Generated Daily Reports."

    now = datetime.now()

    start_time = now.replace(hour=15, minute=40, second=0, microsecond=0)
    end_time = (start_time + timedelta(days=1)).replace(hour=9, minute=30, second=0, microsecond=0)

    if start_time <= now < end_time:
        return True ,"Valid Time for generating daily Reports"
    return False, "You can't generate reports at this time. Try again at valid time"

# Example usage
if is_time_valid_for_daily_report():
    print("Current time is within the range!")
else:
    print("Current time is outside the range!")



def is_time_valid_for_weekly_report():
    now = datetime.now()
    day_of_week = now.weekday()  # Monday=0, Sunday=6

    if day_of_week == 4:
        friday_time = now.replace(hour=15, minute=40, second=0, microsecond=0)
        if now >= friday_time:
            return True

    elif day_of_week == 0:
        monday_time = now.replace(hour=9, minute=0, second=0, microsecond=0)
        if now >= monday_time:
            return True

    elif day_of_week == 5 or day_of_week == 6:

        return True

    return False


def get_report_date():

    now = datetime.now()
    date_format = "%d/%m/%Y"

    # 0=Monday, 6=Sunday
    weekday = now.weekday()
    hour = now.hour
    minute = now.minute

    if weekday in [0, 1, 2, 3]:

        if hour < 9 or (hour == 9 and minute == 0):
            next_day = now
        elif hour >= 16 or (hour == 15 and minute >= 40):
            next_day = now + timedelta(days=1)
        else:
            return "-"

    else:
        days_until_monday = (7 - weekday) % 7
        next_day = now + timedelta(days=days_until_monday)

    return next_day.strftime(date_format)


print("Current time "+get_report_date())


def get_row_order_data():
    row_order_data = {
  "NIFTY 50": 2,
  "NIFTY NEXT 50": 3,
  "NIFTY 100": 4,
  "NIFTY 200": 5,
  "NIFTY 500": 6,
  "NIFTY MIDCAP 50": 7,
  "NIFTY MIDCAP 100": 8,
  "NIFTY SMLCAP 100": 9,
  "INDIA VIX": 10,
  "NIFTY MIDCAP 150": 11,
  "NIFTY SMLCAP 50": 12,
  "NIFTY SMLCAP 250": 13,
  "NIFTY MIDSML 400": 14,
  "NIFTY500 MULTICAP": 15,
  "NIFTY LARGEMID250": 16,
  "NIFTY MID SELECT": 17,
  "NIFTY TOTAL MKT": 18,
  "NIFTY MICROCAP250": 19,
  "NIFTY500 LMS EQL": 20,
  "NIFTY BANK": 21,
  "NIFTY AUTO": 22,
  "NIFTY FIN SERVICE": 23,
  "NIFTY FINSRV25 50": 24,
  "NIFTY FMCG": 25,
  "NIFTY IT": 26,
  "NIFTY MEDIA": 27,
  "NIFTY METAL": 28,
  "NIFTY PHARMA": 29,
  "NIFTY PSU BANK": 30,
  "NIFTY PVT BANK": 31,
  "NIFTY REALTY": 32,
  "NIFTY HEALTHCARE": 33,
  "NIFTY CONSR DURBL": 34,
  "NIFTY OIL AND GAS": 35,
  "NIFTY MIDSML HLTH": 36,
  "NIFTY FINSEREXBNK": 37,
  "NIFTY MS FIN SERV": 38,
  "NIFTY MS IT TELCM": 39,
  "NIFTY DIV OPPS 50": 40,
  "NIFTY GROWSECT 15": 41,
  "NIFTY100 QUALTY30": 42,
  "NIFTY50 VALUE 20": 43,
  "NIFTY50 TR 2X LEV": 44,
  "NIFTY50 PR 2X LEV": 45,
  "NIFTY50 TR 1X INV": 46,
  "NIFTY50 PR 1X INV": 47,
  "NIFTY50 DIV POINT": 48,
  "NIFTY ALPHA 50": 49,
  "NIFTY50 EQL WGT": 50,
  "NIFTY100 EQL WGT": 51,
  "NIFTY100 LOWVOL30": 52,
  "NIFTY200 QUALTY30": 53,
  "NIFTY ALPHALOWVOL": 54,
  "NIFTY200MOMENTM30": 55,
  "NIFTY M150 QLTY50": 56,
  "NIFTY200 ALPHA 30": 57,
  "NIFTYM150MOMNTM50": 58,
  "NIFTY500MOMENTM50": 59,
  "NIFTYMS400 MQ 100": 60,
  "NIFTYSML250MQ 100": 61,
  "NIFTY TOP 10 EW": 62,
  "NIFTY AQL 30": 63,
  "NIFTY AQLV 30": 64,
  "NIFTY HIGHBETA 50": 65,
  "NIFTY LOW VOL 50": 66,
  "NIFTY QLTY LV 30": 67,
  "NIFTY SML250 Q50": 68,
  "NIFTY TOP 15 EW": 69,
  "NIFTY100 ALPHA 30": 70,
  "NIFTY200 VALUE 30": 71,
  "NIFTY500 EW": 72,
  "NIFTY MULTI MQ 50": 73,
  "NIFTY500 VALUE 50": 74,
  "NIFTY TOP 20 EW": 75,
  "NIFTY COMMODITIES": 76,
  "NIFTY CONSUMPTION": 77,
  "NIFTY CPSE": 78,
  "NIFTY ENERGY": 79,
  "NIFTY INFRA": 80,
  "NIFTY100 LIQ 15": 81,
  "NIFTY MID LIQ 15": 82,
  "NIFTY MNC": 83,
  "NIFTY PSE": 84,
  "NIFTY SERV SECTOR": 85,
  "NIFTY100ESGSECLDR": 86,
  "NIFTY IND DIGITAL": 87,
  "NIFTY100 ESG": 88,
  "NIFTY INDIA MFG": 89,
  "NIFTY TATA 25 CAP": 90,
  "NIFTY MULTI MFG": 91,
  "NIFTY MULTI INFRA": 92,
  "NIFTY IND DEFENCE": 93,
  "NIFTY IND TOURISM": 94,
  "NIFTY CAPITAL MKT": 95,
  "NIFTY EV": 96,
  "NIFTY NEW CONSUMP": 97,
  "NIFTY CORP MAATR": 98,
  "NIFTY MOBILITY": 99,
  "NIFTY100 ENH ESG": 100,
  "NIFTY COREHOUSING": 101,
  "NIFTY HOUSING": 102,
  "NIFTY IPO": 103,
  "NIFTY MS IND CONS": 104,
  "NIFTY NONCYC CONS": 105,
  "NIFTY RURAL": 106,
  "NIFTY SHARIAH 25": 107,
  "NIFTY TRANS LOGIS": 108,
  "NIFTY50 SHARIAH": 109,
  "NIFTY500 SHARIAH": 110,
  "NIFTY GS 8 13YR": 111,
  "NIFTY GS 10YR": 112,
  "NIFTY GS 10YR CLN": 113,
  "NIFTY GS 4 8YR": 114,
  "NIFTY GS 11 15YR": 115,
  "NIFTY GS 15YRPLUS": 116,
  "NIFTY GS COMPSITE": 117,
  "BHARATBOND-APR25": 118,
  "BHARATBOND-APR30": 119,
  "BHARATBOND-APR31": 120,
  "BHARATBOND-APR32": 121,
  "BHARATBOND-APR33": 122
}
    return row_order_data
