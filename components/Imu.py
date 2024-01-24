import time
import busio
import board
import adafruit_bno08x
import RPi.GPIO as GPIO
from adafruit_bno08x.i2c import BNO08X_I2C

class BNO085:
    def __init__(self, i2c_address):
        GPIO.setmode(GPIO.BCM)
        self.i2c_address = i2c_address
        self.i2c_bus = busio.I2C(board.SCL, board.SDA)
        self.bno = BNO08X_I2C(self.i2c_bus, address=self.i2c_address)

        self.enable_sensor_features()

    def enable_sensor_features(self):
        self.bno.enable_feature(adafruit_bno08x.BNO_REPORT_ACCELEROMETER)
        self.bno.enable_feature(adafruit_bno08x.BNO_REPORT_GYROSCOPE)
        self.bno.enable_feature(adafruit_bno08x.BNO_REPORT_MAGNETOMETER)
        self.bno.enable_feature(adafruit_bno08x.BNO_REPORT_ROTATION_VECTOR)

    def read_acceleration(self):
        accel_x, accel_y, accel_z = self.bno.acceleration
        return {"accel_x": accel_x, "accel_y": accel_y, "accel_z": accel_z}

    def read_gyro(self):
        gyro_x, gyro_y, gyro_z = self.bno.gyro
        return {"gyro_x": gyro_x, "gyro_y": gyro_y, "gyro_z": gyro_z}

    def read_magnetometer(self):
        mag_x, mag_y, mag_z = self.bno.magnetic
        return {"mag_x": mag_x, "mag_y": mag_y, "mag_z": mag_z}

    def read_rotation_vector(self):
        quat_i, quat_j, quat_k, quat_real = self.bno.quaternion
        return {"quat_i": quat_i, "quat_j": quat_j, "quat_k": quat_k, "quat_real": quat_real}

if __name__ == "__main__":
    bno085_sensor = BNO085(i2c_address=0x4A)  # Update the I2C address

    acceleration = bno085_sensor.read_acceleration()
    print("Acceleration:")
    print(f"X: {acceleration['accel_x']}  Y: {acceleration['accel_y']} Z: {acceleration['accel_z']}  m/s^2")

    gyro = bno085_sensor.read_gyro()
    print("Gyro:")
    print(f"X: {gyro['gyro_x']}  Y: {gyro['gyro_y']} Z: {gyro['gyro_z']} rads/s")

    magnetometer = bno085_sensor.read_magnetometer()
    print("Magnetometer:")
    print(f"X: {magnetometer['mag_x']}  Y: {magnetometer['mag_y']} Z: {magnetometer['mag_z']} uT")

    rotation_vector = bno085_sensor.read_rotation_vector()
    print("Rotation Vector Quaternion:")
    print(f"I: {rotation_vector['quat_i']}  J: {rotation_vector['quat_j']} K: {rotation_vector['quat_k']}  Real: {rotation_vector['quat_real']}")
    
