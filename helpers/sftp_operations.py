from asyncio import subprocess
import os
import requests

from helpers.clipboard_operations import get_clean_clipboard
from helpers.utils import parse_case_number



# WinSCP config
winscp_path = os.environ.get("WINSCP_PATH")
sftp_url = os.environ.get("SFTP_URL")
sftp_user = os.environ.get("SFTP_USER")
sftp_pass = os.environ.get("SFTP_PASS")

email = os.environ.get("EMAIL")
sftp_create_url = os.environ.get("SFTP_CREATE_URL")



# Creates SFTP account case number in clipboard
def create_sftp():
    case_number = get_clean_clipboard()
    case_number = parse_case_number(case_number)
    data = {
        'username': case_number,
        'email': email,
        'submit': 'Create User'
    }
    headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Content-Length': str(len(data)),
    }

    http_request = requests.post(sftp_create_url, data=data, headers=headers)
    print(http_request.status_code)
    print(http_request.json())

def renew_sftp():
    print('renew sftp')

def open_winscp():
    # Get case number
    case_number = get_clean_clipboard()
    case_number = parse_case_number(case_number)

    try:
        command = f'{winscp_path} sftp://{sftp_user}:{sftp_pass}@{sftp_url}/{case_number}/outgoing'
    except:
        print('Failed to open sftp: ' + command)
    subprocess.run(command)