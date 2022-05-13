import keyboard

from tkinter import *
from tkinter import ttk


from helpers.Button import Button
from helpers.os_operations import create_open_folder
from helpers.sftp_operations import create_sftp, open_winscp, renew_sftp
from helpers.clipboard_operations import get_clean_clipboard, is_valid_clipboard 
from helpers.utils import parse_case_number

# Default keys to activate functions (ctrl + alt + <key>)
folder_create_key = 'v'
sftp_create_key = 'f'
sftp_renew_key = 'g'
open_winscp_key = 'e'


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