import sys
import re
import time
import threading
from collections import deque
from math import radians, sin, cos, sqrt, atan2

library_path = '../components'
sys.path.append(library_path)

from Imu import BNO085
from UltrasonicSensor import UltrasonicSensor
from Sim import Modem
from MotorController import MobilePlatform
from Box import Box
from Camera import Camera

class AutonomousNavigator:
    def __init__(self, mobile_platform, box_manager, modem, camera):
        self.mobile_platform = mobile_platform
        self.box_manager = box_manager
        self.sim = modem
        self.camera = camera
        self.imu = BNO085(0x4A)
        self.l_ultrasonic = UltrasonicSensor(23, 11)
        self.f_ultrasonic = UltrasonicSensor(25, 9)
        self.r_ultrasonic = UltrasonicSensor(24, 27)
        
        self.ultrasonic_thread = threading.Thread(target=self.monitor_ultrasonic)
        self.camera_thread = threading.Thread(target=self.monitor_camera)
        self.gps_thread = threading.Thread(target=self.monitor_gps_coordinates)
        self.movement_thread = threading.Thread(target=self.control_movement)

        self.ultrasonic_queue = deque()
        self.camera_queue = deque()
        self.gps_queue = deque()
        self.activated = False

        self.route = []
        self.last_coordinates = {'lat' : 0, 'lng' : 0}
        self.customer_number = ''

    def start(self):
        self.activated = True
        self.mobile_platform.open_serial()

    def stop(self):
        self.activated = False
        self.mobile_platform.stop_motors()
        self.mobile_platform.close_serial()
        self.stop_navigation_threads()

    def start_navigation_threads(self):
        self.ultrasonic_thread.start()
        self.camera_thread.start()
        self.gps_thread.start()
        self.movement_thread.start()

    def stop_navigation_threads(self):
        if self.movement_thread.is_alive():
            self.ultrasonic_thread.stop()
            self.camera_thread.stop()
            self.gps_thread.stop()
            self.movement_thread.stop()

            self.ultrasonic_thread.join()
            self.camera_thread.join()
            self.gps_thread.join()
            self.movement_thread.join()

    def indicate_arival(self):
        localization = self.get_gps_data()
        message = f'Robot arrived, the parcel is waiting to be picked up at coordinates: {localization}'
        self.sim.open_serial()
        self.sim.send_sms(self.customer_number, message)
        self.sim.close_serial()
        self.box_manager.start_oppening_procedure()

    def indicate_onjourney(self):
        self.box_manager.generate_password()
        password = self.box_manager.get_password()
        message = f'Package is on the way, your access key to pickup the parcel: {password}'
        self.sim.open_serial()
        self.sim.send_sms(self.customer_number, message)
        self.sim.close_serial()

    def get_path(self, route):
        path = []
        for step in route[0]['steps']:
            points = step.get('path', [])
            points.extend(path)
        formatted_path = [{'lat': round(point['lat'], 5), 'lng': round(point['lng'], 5)} for point in path]
        self.route = formatted_path

    def get_imu_data(self):
        magnetometer = self.imu.read_magnetometer()
        return magnetometer

    def get_ultrasonic_data(self):
        left_distance = self.l_ultrasonic.get_distance()
        front_distance = self.f_ultrasonic.get_distance()
        right_distance = self.r_ultrasonic.get_distance()
        return {'left' : left_distance, 'front' : front_distance, 'right' : right_distance}

    def get_gps_data(self):
        self.sim.open_serial()
        gps_data = self.sim.read_gps_data()
        if gps_data['lat'] is not None and gps_data['lng'] is not None:
            gps_data = {'lat': round(gps_data['lat'], 5), 'lng': round(gps_data['lng'], 5)}
        self.sim.close_serial()
        return gps_data

    def get_camera_data(self):
        frame = camera.read_frame()
        if frame is not None:
            unwraped_frame = camera.unwrap_fisheye(frame)
            sidewalk_frame, left_value, right_value = camera.detect_sidewalk(unwraped_frame)
            return {'width' : sidewalk_frame.shape[1], 'left' : left_value, 'right' : right_value}
        else:
            return {'width' : 0, 'left' : 0, 'right' : 0}
        
    def get_next_path_coordinates(self):
        if len(self.route) != 0:
            self.route.pop(0)
            return self.route[0]
        else:
            return None

    def get_destination_coordinates(self):
        if len(self.route) != 0:
            return self.route[-1]
        else:
            return None

    def calculate_distance(cord1, cord2):
        R = 6371
        lat1, lng1, lat2, lng2 = map(radians, [cord1['lat'], cord1['lng'], cord2['lat'], cord2['lng']])
        dlat = lat2 - lat1
        dlng = lng2 - lng1

        # Haversine formula
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlng / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        return distance

 
    def calculate_value_difference(self, value1, value2):
        difference = (value2 - value1 + 360) % 360
        return difference

    def turn_around(self):
        start_orientation = self.get_imu_data()
        actual_orientation = self.get_imu_data()
        self.mobile_platform.send_move_command('L', 150)
        while self.calculate_value_difference(start_orientation['mag_x'], actual_orientation['mag_x']) < 180:
            actual_orientation = self.get_imu_data()
        self.mobile_platform.send_move_command('F', 255)

    def change_path_to_avoid_object(self, direction):
        start_orientation = self.get_imu_data()
        actual_orientation = self.get_imu_data()
        if direction == 'left':
            self.mobile_platform.send_move_command('L', 150)
            while self.calculate_value_difference(start_orientation['mag_x'], actual_orientation['mag_x']) < 90:
                actual_orientation = self.get_imu_data()
            self.mobile_platform.send_move_command('F', 255)
            time.sleep(0.2)
            start_orientation = self.get_imu_data()
            self.mobile_platform.send_move_command('R', 150)
            actual_orientation = self.get_imu_data()
            while self.calculate_value_difference(actual_orientation['mag_x'], start_orientation['mag_x']) < 90:
                actual_orientation = self.get_imu_data()
            self.mobile_platform.send_move_command('F', 255)

        elif direction == 'right':
            self.mobile_platform.send_move_command('R', 150)
            while self.calculate_value_difference(actual_orientation['mag_x'], start_orientation['mag_x']) < 90:
                actual_orientation = self.get_imu_data()
            self.mobile_platform.send_move_command('F', 255)
            time.sleep(0.2)
            start_orientation = self.get_imu_data()
            self.mobile_platform.send_move_command('R', 150)
            actual_orientation = self.get_imu_data()
            while self.calculate_value_difference(start_orientation['mag_x'] - actual_orientation['mag_x']) < 90:
                actual_orientation = self.get_imu_data()
            self.mobile_platform.send_move_command('F', 255)

    def monitor_ultrasonic(self):
        while self.activated:
            ultrasonic_data = self.get_ultrasonic_data()
            self.ultrasonic_queue.append(ultrasonic_data)
            time.sleep(0.1)

    def monitor_camera(self):
        while self.activated:
            camera_data = self.get_camera_data()
            self.camera_queue.append(camera_data)
            time.sleep(0.1)

    def monitor_gps_coordinates(self):
        while self.activated:
            gps_data = self.get_gps_data()
            self.gps_queue.append(gps_data)
            time.sleep(0.1)
            
    def control_movement(self):
        self.indicate_onjourney()
        destination_coordinates = self.get_destination_coordinates()
        path_step = self.get_next_path_coordinates()
        
        while self.activated:
            ultrasonic_data = self.ultrasonic_queue.pop()
            camera_data = self.camera_queue.pop()
            gps_data = self.gps_queue.pop()

            if gps_data == path_step:
                if gps_data == destination_coordinates:
                    self.mobile_platform.stop_motors()
                    self.indicate_arival()
                    break
                else:
                    path_step = self.get_next_path_coordinates()
                    continue

            last_distance = self.calculate_distance(self.last_coordinates, path_step)
            actual_distance = self.calculate_distance(gps_data, path_step)
            if actual_distance > last_distance:
                self.turn_around()
                continue
            self.last_coordinates = gps_data

            if any(value is not None and value < 50 for value in ultrasonic_data.values()):
                self.mobile_platform.stop_motors()
                continue

            if ultrasonic_data['front'] < 150 and ultrasonic_data['left'] < 150:
                self.change_path_to_avoid_object('right')
                continue

            if ultrasonic_data['front'] < 150:
                self.change_path_to_avoid_object('left')
                continue

            if camera_data['width']/camera_data['left'] < 4:
                mobile_platform.send_move_command('E', 255)
                continue

            if camera_data['right']/camera_data['width'] < 0.75:
                mobile_platform.send_move_command('Q', 255)
                continue

            mobile_platform.send_move_command('F', 255)
            time.sleep(0.1)
            
        self.mobile_platform.stop_motors()

    def navigate(self, customer_number):
        self.customer_number = customer_number
        self.start_navigation_threads()

if __name__ == "__main__":
    mobile_platform = MobilePlatform()
    box_manager = Box()
    modem = Modem()
    camera = Camera()
    navigator = AutonomousNavigator(mobile_platform, box_manager, modem, camera)
    navigator.start()
    navigator.navigate('123')
