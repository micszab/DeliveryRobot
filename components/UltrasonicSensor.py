import RPi.GPIO as GPIO
import time

class UltrasonicSensor:
    def __init__(self, trig_pin, echo_pin):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        self.timeout = 5

        self.setup_pins()

    def setup_pins(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def trig_signal(self):
        GPIO.output(self.trig_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trig_pin, False)

    def get_distance(self):
        distance = None
        self.trig_signal()
        pulse_start = None
        pulse_end = None

        while GPIO.input(self.echo_pin) == 0:
            pulse_start = time.time()
        
        while GPIO.input(self.echo_pin) == 1:
            if (pulse_start is not None) and (time.time() - pulse_start > self.timeout):
                break
            pulse_end = time.time()

        if pulse_start and pulse_end:
            pulse_duration = pulse_end - pulse_start
            distance = round(pulse_duration * 17150, 2)

        return distance

if __name__ == "__main__":
    sensor_pins = [(23, 11), (25, 9), (24, 27)]

    sensors = [UltrasonicSensor(trig_pin, echo_pin) for trig_pin, echo_pin in sensor_pins]

    try:
        while True:
            for idx, sensor in enumerate(sensors):
                distance = sensor.get_distance()
                print(f"Sensor {idx + 1}: {distance} cm")
            time.sleep(1)

    except KeyboardInterrupt:
        print("KeyboardInterrupt has been caught.")
        GPIO.cleanup()
