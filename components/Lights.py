import RPi.GPIO as GPIO
import time

class LightController:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.is_activated = False

    def switch_mode(self):
        if self.is_activated:
            GPIO.output(self.pin, GPIO.LOW)
            self.is_activated = False
        else:
            GPIO.output(self.pin, GPIO.HIGH)
            self.is_activated = True

    def cleanup(self):
        GPIO.cleanup()
        print("GPIO cleanup completed.")

# Example usage
if __name__ == "__main__":
    light_pin = 17
    light = LightController(light_pin)
    light.switch_mode()
