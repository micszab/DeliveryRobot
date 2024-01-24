import RPi.GPIO as GPIO
import time

class Keypad4x4:
    def __init__(self):
        self.rows = [12, 16, 20, 21]
        self.cols = [26, 19, 13, 5]
        self.keys = [
        ['1', '2', '3', 'A'],
        ['4', '5', '6', 'B'],
        ['7', '8', '9', 'C'],
        ['*', '0', '#', 'D']
        ]
        GPIO.setmode(GPIO.BCM)

        # Setup rows as outputs and columns as inputs
        for row_pin in self.rows:
            GPIO.setup(row_pin, GPIO.OUT)
            GPIO.output(row_pin, GPIO.HIGH)

        for col_pin in self.cols:
            GPIO.setup(col_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    def __del__(self):
        if hasattr(self, 'rows') and hasattr(self, 'cols'):
            GPIO.cleanup()

    def get_key(self):
        while True:
            for i in range(len(self.rows)):
                GPIO.output(self.rows[i], GPIO.LOW)

                row_state = [GPIO.input(row) for row in self.rows]
                col_state = [GPIO.input(col) for col in self.cols]

                for j in range(len(self.cols)):
                    key_state = GPIO.input(self.cols[j])
                    if key_state == GPIO.LOW:
                        key = self.keys[i][j]
                        time.sleep(0.05)
                        self.wait_for_key_release(self.cols[j])
                        return key

                GPIO.output(self.rows[i], GPIO.HIGH)
                time.sleep(0.05)
            return None

    def wait_for_key_release(self, row):
        while GPIO.input(row) == GPIO.LOW:
            time.sleep(0.05)
            

# Example usage
if __name__ == "__main__":
    keypad = Keypad4x4()

    try:
        while True:
            pressed_key = keypad.get_key()
            print("Pressed Key:", pressed_key)

    except KeyboardInterrupt:
        print("KeyboardInterrupt has been caught.")

