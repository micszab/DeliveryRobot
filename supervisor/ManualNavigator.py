import sys
import time

library_path = '../components'
sys.path.append(library_path)

from MotorController import MobilePlatform
from Box import Box
from Lights import LightController

class ManualNavigator:
    def __init__(self, mobile_platform, box_manager):
        self.motor_controller = mobile_platform
        self.box_manager = box_manager
        self.lights = LightController()
        self.activated = False

    def start(self):
        self.activated = True

    def stop(self):
        self.activated = False

    def is_activated(self):
        return self.activated

    def open_box(self):
        if self.activated:
            self.box_manager.open_box()

    def switch_lights(self):
        if self.activated:
            self.lights.switch_mode()

    def stop_motors(self):
        if self.activated:
            self.motor_controller.stop_motors()

    def move_forward(self):
        if self.activated:
            self.motor_controller.send_move_command('F', 255)

    def move_backward(self):
        if self.activated:
            self.motor_controller.send_move_command('B', 255)

    def move_left_up(self):
        if self.activated:
            self.motor_controller.send_move_command('Q', 255)

    def move_left_down(self):
        if self.activated:
            self.motor_controller.send_move_command('Z', 255)

    def move_right_up(self):
        if self.activated:
            self.motor_controller.send_move_command('E', 255)

    def move_right_down(self):
        if self.activated:
            self.motor_controller.send_move_command('C', 255)

    def turn_left(self):
        if self.activated:
            self.motor_controller.send_move_command('L', 200)
            time.sleep(1)
            self.motor_controller.stop_motors()

    def turn_right(self):
        if self.activated:
            self.motor_controller.send_move_command('R', 200)
            time.sleep(1)
            self.motor_controller.stop_motors()


if __name__ == "__main__":
    mobile_platform = MobilePlatform()
    box_manager = Box()

    manual_controller = ManualNavigator(mobile_platform, box_manager)
    self.manual_controller.start()
