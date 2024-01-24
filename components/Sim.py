import serial
import time

class Modem:
    def __init__(self):
        self.serial_addr = '/dev/ttyUSB4'
        self.serial_port = None

    def open_serial(self):
        self.serial_port = serial.Serial(self.serial_addr, 9600, timeout=1)
        self.serial_port.flush()
        self.serial_port.reset_input_buffer()

    def close_serial(self):
        self.serial_port.close()

    def send_at_command(self, command):
        #print(f"Sending: {command}")
        if self.serial_port is not None:
            self.serial_port.write((command + '\r\n').encode())
            time.sleep(1)

    def get_response(self):
        response = self.serial_port.read(self.serial_port.in_waiting).decode().split(' ')
        return response

    def send_sms(self, recipient_number, sms_message):
        # Set SMS text mode
        self.send_at_command("AT+CMGF=1")
        # Set recipient phone number
        self.send_at_command(f'AT+CMGS="{recipient_number}"')
        # Send the SMS message
        self.send_at_command( sms_message + chr(26))
        time.sleep(1)
        resp = self.get_response()

    def dms_to_decimal(self, degrees, direction):
        degrees = degrees.lstrip('0')
        if degrees:
            decimal_degrees = float(degrees[:2]) + float(degrees[2:]) / 60
            if direction in ['S', 'W']:
                decimal_degrees = -decimal_degrees
        else:
            decimal_degrees = None
        return decimal_degrees

    def read_gps_data(self):
        self.send_at_command('AT+CGPSINFO')
        time.sleep(1)
        gps_data = self.get_response()
        gps_values = gps_data[-1]
        gps_long_lat = gps_values.split(',')
        latitude_dms, latitude_direction, longitude_dms, longitude_direction = gps_long_lat[:4]
        latitude_decimal = self.dms_to_decimal(latitude_dms, latitude_direction)
        longitude_decimal = self.dms_to_decimal(longitude_dms, longitude_direction)
        if latitude_decimal and longtitude_decimal is not None:
            return {'lat' : float(latitude_decimal), 'lng' : float(longitude_decimal)}
        else:
            return {'lat' : None, 'lng' : None}

if __name__ == "__main__":
    recipient_number = "+48501084604"
    sms_message = "misiu"

    modem = Modem()
    modem.open_serial()
    print(modem.read_gps_data())
    #modem.send_sms(recipient_number, sms_message)
    modem.close_serial()
