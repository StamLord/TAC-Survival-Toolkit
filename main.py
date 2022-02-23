import getpass
import requests
import win32clipboard
import keyboard
import os
import subprocess
import shutil
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from tkinter import *
from tkinter import ttk

# Default keys to activate functions (ctrl + alt + <key>)
folder_create_key = 'v'
sftp_create_key = 'f'
sftp_renew_key = 'g'
open_winscp_key = 'e'

# Paths and URLs
ad_user = getpass.getuser()
srs_path = "\\\\planet\\support\\SRs\\"
sftp_create_url = 'https://ftp-win.checkpoint.com:8181/TACusers/newuser.asp'
email = ad_user + '@checkpoint.com'
downloads_path = "C:\\Users\\" + ad_user + "\\Downloads\\"

log_file_extensions = ["log", "elg", "txt"]
img_file_extensions = ["jpg", "jpeg", "gif", "png"]
ignore_file_extensions = ["crdownload"]

# WinSCP config
winscp_path = 'C:\Program Files (x86)\WinSCP\WinSCP.exe'
sftp_url = 'ftp.checkpoint.com'
sftp_user = 'tacuser'
sftp_pass = 'M2bxu9GDIG!367'

# Get data from clipboard
def get_clipboard():
    win32clipboard.OpenClipboard()
    data = ''
    try:
        data = win32clipboard.GetClipboardData()
    except:
        #print("ERROR: Could not get clipboard data")
        pass
    win32clipboard.CloseClipboard()
    return data

# Removes special characters from string
def clean_clipboard(str):
    str = str.rstrip() # Remove whitespaces
    return str.rstrip('\r\n') # Remove new lines

# Gets and cleans data from clipboard
def get_clean_clipboard():
    return clean_clipboard(get_clipboard())

# Fix a string to fit the format: 6-0000000000
def parse_case_number(case_number):
    case_number = case_number.rstrip('\n')
    # If not enough numbers, fill with zeroes
    while len(case_number) < 10:
        case_number = '0' + case_number

    # If we are missing right side, add [6-]
    if len(case_number) == 10:
        case_number = '6-' + case_number

    # If lengh is correct we add [-] or [6]
    if len(case_number) == 11:
        if '-' in case_number:
            case_number = '6' + case_number
        else:
            case_number = case_number[0] + '-' + case_number[1:]
    return case_number

def is_valid_clipboard(clipboard):
    split = clipboard.split('-')
    for c in split:
        if not c.isdecimal():
            return False
    return True

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
    if path is None:
        case_number = get_clean_clipboard()
        case_number = parse_case_number(case_number)
        path = srs_path + case_number

    if not os.path.exists(path):
        create_folder(path)
    open_folder(path) # We open the folder if it exists or if we created it

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

# Contains logic for input processing
# All keys require ctrl + alt as well to be processed
class Button:
    def __init__(self, key, function):
        self.key = key
        self.function = function
        self.is_pressed_once = False

    def process(self):
        if keyboard.is_pressed('ctrl') and keyboard.is_pressed('alt'):
            if keyboard.is_pressed(self.key) and not self.is_pressed_once:
                print('Key [' + self.key + '] is pressed')
                print('Running function:' + self.function.__name__)
                self.function()
                self.is_pressed_once = True
            elif not keyboard.is_pressed(self.key):
                self.is_pressed_once = False
        else:
            self.is_pressed_once = False

# All buttons listen for ctrl + alt and a custom key
folders_button = Button(folder_create_key, create_open_folder)
sftp_create_button = Button(sftp_create_key, create_sftp)
sftp_renew_button = Button(sftp_renew_key, renew_sftp)
open_winscp_button = Button(open_winscp_key, open_winscp)

# Single processing of all buttons
def buttons_process():
    try:
        folders_button.process()
        sftp_create_button.process()
        sftp_renew_button.process()
        open_winscp_button.process()
    except Exception as e:
        print(e)

#<editor-fold desc="TKinter GUI -- Optional, can be deleted">

root = Tk()
root.title('TAC Survival Toolkit')


# Valid/Invalid Text
valid_text = StringVar()
clipboard_widget = Label(root, textvariable=valid_text)
clipboard_widget.config(fg='red', height=1, width=30)
clipboard_widget.grid(row=0, column=1)

# Current Clipboard UI
Label(root, text="Clipboard: ").grid(row=1, column=0)
clipboard_text = StringVar()
clipboard_widget = Label(root, textvariable=clipboard_text)
clipboard_widget.config(fg='purple', height=1, width=30)
clipboard_widget.grid(row=1, column=1)

# Parsed Text
parsed_text = StringVar()
clipboard_widget = Label(root, textvariable=parsed_text)
clipboard_widget.config(fg='blue', height=1, width=30)
clipboard_widget.grid(row=2, column=1)

# Parse clipboard for UI
def string_ui_parse(str, limit):
    return str[0:limit]

# Constantly Updates clipboard text after first call
def update_clipboard_gui():
    clipboard = get_clean_clipboard()
    clipboard_text.set(string_ui_parse(clipboard,50))

    if is_valid_clipboard(clipboard):
        valid_text.set('')
        parsed_text.set(parse_case_number(clipboard))
    else:
        valid_text.set('Invalid Input')
        parsed_text.set('')

    root.after(500, update_clipboard_gui)

# Starts clipboard label update loop
update_clipboard_gui()

# Returns true if key is no assigned to any other button
def verify_unique_key(key):
    keys = folders_button.key + sftp_create_button.key + sftp_renew_button.key
    return key not in keys

def configure_button(button, text):
    text.set('Press any key...')
    root.update_idletasks() # Allows label to update
    new_key = keyboard.read_key()
    if(verify_unique_key(new_key)):
        button.key = new_key
    text.set('ctrl+alt+' + button.key)

# Space
Label(root, text=" ").grid(row=3, column=0)

# Creates a ui button to configure a hotkey button
#Example: <label_text> [Configure] ctrl+alt+<key>
def create_ui_button(label_text, row, button):
    # Button name/description
    Label(root, text=label_text).grid(row=row, column=0, stick='w')
    # Configure button
    btn = ttk.Button(root, text="Configure", command=lambda: configure_button(button, create_folder_key_text))
    btn.grid(row=row, column=1, stick='e')
    # Current key combination
    create_folder_key_text = StringVar(value='     ctrl+alt+' + button.key + '     ')
    label = Label(root, textvariable=create_folder_key_text)
    label.config(width=10)
    label.grid(row=row, column=2)

# UI Buttons
create_ui_button("Create/Open Folders", 4, folders_button)
create_ui_button("Create SFTP", 5, sftp_create_button)
create_ui_button("Renew SFTP", 6, sftp_renew_button)
create_ui_button("Open WinSCP", 7, open_winscp_button)

# Constantly keeps processing buttons
def process_buttons_loop():
    buttons_process()
    root.after(1, process_buttons_loop)

# Starts button process loop
process_buttons_loop()

# Watchdog Setup
def on_created(event):
    #print(f"New file in {downloads_path}: {event.src_path}")
    file_path = event.src_path
    file_name = file_path.split('\\')[-1] # Split by '\' and take last element
    if '_' not in file_name:
        return

    split_file_name = file_name.split('_')
    sr_number = split_file_name[0] # First member is the SR number

    # SR should always contain 12 digits (with '-')
    if len(sr_number) != 12:
        return

    # Make sure we have only 2 parts if we split by '-'
    sr_decimals = sr_number.split('-')
    if len(sr_decimals) != 2:
        return

    # Make sure both parts of sr number are only numbers
    if not sr_decimals[0].isdecimal() or not sr_decimals[1].isdecimal():
        return

    real_file_name_list = split_file_name[2:] # Get the rest of the file name (2nd member is salesforce junk so we skip it)
    real_file_name = ''
    for index, word in enumerate(real_file_name_list):
        real_file_name += word
        if (index < len(real_file_name_list) - 1):
            real_file_name += '_'
    ext = real_file_name.split('.')[-1] # Splt by '.' and get last element
    ext = ext.lower() # We compare to lowercase extension list

    # Ignore temporary download files
    if ext in ignore_file_extensions:
        return

    # Validate SR number
    if(len(sr_number) != 12 or '-' not in sr_number):
        return

    new_path = srs_path + sr_number+"\\"
    # Check if log file
    if ext in log_file_extensions:
        new_path = new_path + "Logs\\"
    # Check if image
    elif ext in img_file_extensions:
        new_path = new_path + "Screenshots\\"

    # Create folder if doesn't exist
    if not os.path.exists(new_path):
        create_folder(new_path)

    # Build final path with filename
    file_new_path = new_path + real_file_name

    # Move File
    print("Moving file: " + event.src_path + " => " + file_new_path)
    try:
        shutil.move(event.src_path, file_new_path)
    except:
        print("ERROR: Not able to move file.")

patterns = ['*']
ignore_patterns = None
ignore_directories = False
case_sensitive = True
wd_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
wd_event_handler.on_created = on_created
wd_event_handler.on_modified= on_created

wd_observer = Observer()
wd_observer.schedule(wd_event_handler, downloads_path, recursive=False)
wd_observer.start()

root.mainloop()

# End of Tkinter GUI

#</editor-fold>

# Code is blocked. Remove GUI block above for non gui app
#if __name__ == '__main__':
#    while True:
#        buttons_process()