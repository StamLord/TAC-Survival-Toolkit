import os

from helpers.clipboard_operations import get_clean_clipboard
from helpers.utils import parse_case_number




# Open folder in File Explorer
def open_folder(path):
    path = os.path.realpath(path)
    print('Opening directory: ' + path)
    os.startfile(path)

# Create a folder
def create_folder(path):
    print('Creating directory:' + path)
    os.makedirs(path)

# Opens a folder if exists or creates based case number in clipboard or passed string
def create_open_folder(path = None):
    srs_path = os.environ.get('SR_PATH')

    if path is None:
        case_number = get_clean_clipboard()
        case_number = parse_case_number(case_number)
        print(srs_path, case_number)
        path = srs_path + case_number

    if not os.path.exists(path):
        create_folder(path)
    open_folder(path) # We open the folder if it exists or if we created it

