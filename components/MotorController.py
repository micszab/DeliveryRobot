import serial
import time

class MobilePlatform:
    def __init__(self):
        self.serial_addr = '/dev/ttyUSB0'
        self.baud_rate = 115200
        self.serial_port = None

    def open_serial(self):
        self.serial_port = serial.Serial(self.serial_addr, self.baud_rate, timeout=1)
        self.serial_port.flush()
        self.serial_port.reset_input_buffer()

    def close_serial(self):
        self.serial_port.close()

    def send_move_command(self, direction, value):
        message = f'<{direction}{value}>'
        print(f'sending {message}')
        self.serial_port.write(message.encode())

    def stop_motors(self):
        direction = 'S'
        value = 0
        message = f'<{direction}{value}>'
        self.serial_port.write(message.encode())


if __name__ == '__main__':
    mobile_platform = MobilePlatform()
    mobile_platform.open_serial()
    try:
        while True:
            mobile_platform.send_move_command('E', 100)
            print('move right up')
            time.sleep(2)
            mobile_platform.send_move_command('S', 0)
            print('stop')
            time.sleep(2)
            mobile_platform.send_move_command('C', 100)
            print('move right down')
            time.sleep(2)
            mobile_platform.send_move_command('S', 0)
            print('stop')
            time.sleep(2)
            mobile_platform.send_move_command('Q', 100)
            print('move left up')
            time.sleep(2)
            mobile_platform.send_move_command('S', 0)
            print('stop')
            time.sleep(2)
            mobile_platform.send_move_command('Z', 100)
            print('move left down')
            time.sleep(2)
            mobile_platform.send_move_command('S', 0)
            print('stop')
            time.sleep(2)
    except KeyboardInterrupt:
        print("KeyboardInterrupt has been caught.")

