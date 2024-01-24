import time
import RPi.GPIO as GPIO

class ServoControl:
    def __init__(self):
        self.gpio_pin = 18
        self.servo_min = 2.5
        self.servo_max = 12.5
        self.pwm = None
        self.setup_gpio()

    def __del__(self):
        if self.pwm is not None:
            self.pwm.stop()
            GPIO.cleanup(self.gpio_pin)

    def setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT)
        if GPIO.gpio_function(self.gpio_pin) == 1:
            existing_pwm = GPIO.PWM(self.gpio_pin, 50)
            existing_pwm.stop()
            GPIO.cleanup(self.gpio_pin)
        self.pwm = GPIO.PWM(self.gpio_pin, 50)
        self.pwm.start(0)

    def move_angle(self, angle):
        pulse_width = self.servo_min + (angle / 180.0) * (self.servo_max - self.servo_min)
        self.pwm.ChangeDutyCycle(pulse_width)
        time.sleep(0.5)

    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    servo = ServoControl()
    try:
        servo.move_angle(60)
        print('servo start 60 degree')
        time.sleep(3)
        servo.move_angle(150)
        print('servo move 90(150) degree')
        time.sleep(3)
    finally:
        del servo
