import os
import sys
import random
import time

from Keypad import Keypad4x4
from Servo import ServoControl
from LcdDisplay import LCD16x2

class Box:
    def __init__(self):
        self.password = ''
        self.keypad = Keypad4x4()
        self.servo = ServoControl()
        self.lcd = LCD16x2()

    def get_password(self):
        return self.password

    def generate_password(self):
        self.password = ''.join(random.choices('0123456789', k=4))

    def confirm_password(self, numbers):
        status = ''
        if self.password == numbers:
            status = 'Correct'
        else:
            status = 'Wrong'
        return status

    def open_box(self):
        self.servo.move_angle(150)
        time.sleep(30)
        self.servo.move_angle(60)

    def start_oppening_procedure(self):
        password_input = ''
        while len(password_input) < 4:
            key = None
            self.lcd.display_on()
            self.lcd.write_string('Enter password:', self.lcd.get_addr_line_1())
            while key is None:
                key = self.keypad.get_key()
            if key == 'A' and len(password_input) > 0:
                password_input = password_input[:-1]
            else:
                password_input = password_input + key
            self.lcd.write_string(password_input, self.lcd.get_addr_line_2())

        status = self.confirm_password(password_input)
        if status == 'Correct':
            self.open_box()
            self.lcd_display_off()
        else:
            self.start_oppening_procedure()
    

if __name__ == '__main__':
    box = BoxManager()
    box.generate_password()
    print(box.get_password())
    box.start_oppening_procedure()
    
