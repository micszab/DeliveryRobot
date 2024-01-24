#!/usr/bin/python
import smbus
import time

class LCD16x2:
    def __init__(self):
        self.I2C_ADDR  = 0x27 # I2C device address
        self.LCD_WIDTH = 16   # Maximum characters per line
        self.LCD_CHR = 1 # Mode - Sending data
        self.LCD_CMD = 0 # Mode - Sending command
        self.LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
        self.LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
        self.LCD_BACKLIGHT  = 0x08  # On
        self.ENABLE = 0b00000100 # Enable bit
        self.DELAY = 0.0005
        
        self.bus = smbus.SMBus(1)

    def get_addr_line_1(self):
        return self.LCD_LINE_1

    def get_addr_line_2(self):
        return self.LCD_LINE_2
       
    def display_off(self):
        self.write_bits(0x01, self.LCD_CMD)

    def display_on(self):
        self.write_bits(0x33, self.LCD_CMD) # 110011 Initialise
        self.write_bits(0x32, self.LCD_CMD) # 110010 Initialise
        self.write_bits(0x06, self.LCD_CMD) # 000110 Cursor move direction
        self.write_bits(0x0C, self.LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
        self.write_bits(0x28, self.LCD_CMD) # 101000 Data length, number of lines, font size
        self.write_bits(0x01, self.LCD_CMD) # 000001 Clear display
        time.sleep(self.DELAY)

    def write_bits(self, bits, mode):
        bits_high = mode | (bits & 0xF0) | self.LCD_BACKLIGHT
        bits_low = mode | ((bits<<4) & 0xF0) | self.LCD_BACKLIGHT
        self.bus.write_byte(self.I2C_ADDR, bits_high)
        self.enable_bits(bits_high)
        self.bus.write_byte(self.I2C_ADDR, bits_low)
        self.enable_bits(bits_low)

    def enable_bits(self, bits):
        time.sleep(self.DELAY)
        self.bus.write_byte(self.I2C_ADDR, (bits | self.ENABLE))
        time.sleep(self.DELAY)
        self.bus.write_byte(self.I2C_ADDR,(bits & ~self.ENABLE))
        time.sleep(self.DELAY)

    def write_string(self, message, line):
        message = message.ljust(self.LCD_WIDTH," ")
        self.write_bits(line, self.LCD_CMD)
        for i in range(self.LCD_WIDTH):
            self.write_bits(ord(message[i]), self.LCD_CHR)

if __name__ == '__main__':
  try:
    lcd = LCD16x2()
    lcd.display_on()
    time.sleep(1)
    lcd.write_string("Enter Password: ", 0x80)
    lcd.write_string("****", 0xC0)
    time.sleep(5)
  except KeyboardInterrupt:
    print("KeyboardInterrupt has been caught.")
  finally:
    lcd.display_off()
