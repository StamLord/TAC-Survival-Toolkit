import os

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

log_file_extensions = ["log", "elg", "txt"]
img_file_extensions = ["jpg", "jpeg", "gif", "png"]
ignore_file_extensions = ["crdownload"]

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
# wd_observer.schedule(wd_event_handler, downloads_path, recursive=False)
