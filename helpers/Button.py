import keyboard

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
