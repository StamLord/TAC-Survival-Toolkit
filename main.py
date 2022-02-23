import getpass
import requests
import keyboard
import os
import subprocess
import shutil

from dotenv import load_dotenv

from bin.main_GUI import root
from bin.watchdog import wd_observer, wd_event_handler

from helpers.Button import Button
from helpers.utils import parse_case_number
from helpers.clipboard_operations import get_clean_clipboard, is_valid_clipboard
from helpers.sftp_operations import create_sftp, open_winscp, renew_sftp
from helpers.os_operations import create_open_folder


# Paths and URLs
# Load .env file
os.environ["AD_USER"] = getpass.getuser()
load_dotenv('./.env')

srs_path = os.environ.get('SR_PATH')
sftp_create_url = os.environ.get("SFTP_CREATE_URL")
email = os.environ.get("EMAIL")
downloads_path = os.environ.get("DOWNLOAD_PATH")

# WinSCP config
# Should be deleted after refactoring SFTP operations
winscp_path = os.environ.get("WINSCP_PATH")
sftp_url = os.environ.get("SFTP_URL")
sftp_user = os.environ.get("SFTP_USER")
sftp_pass = os.environ.get("SFTP_PASS")

wd_observer.schedule(wd_event_handler, downloads_path, recursive=False)
wd_observer.start()

root.mainloop()
