import win32clipboard

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


# Gets data from the clipboard and returns a string without whitespaces from the beginning and end.
def get_clean_clipboard():
    return get_clipboard().strip()

def is_valid_clipboard(clipboard):
    split = clipboard.split('-')
    for c in split:
        if not c.isdecimal():
            return False
    return True