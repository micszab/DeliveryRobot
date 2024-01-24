from flask import Flask, render_template, Response, jsonify
from flask_socketio import SocketIO
import cv2
import imutils
import sys

library_components = '../components'
sys.path.append(library_components)

from Sim import Modem
from Box import Box
from MotorController import MobilePlatform
from Camera import Camera

library_supervisors = '../supervisor'
sys.path.append(library_supervisors)

from ManualNavigator import ManualNavigator
from AutonomousNavigator import AutonomousNavigator

box_manager = BoxManager()
modem = Modem()
mobile_platform = MobilePlatform()
mobile_platform.open_serial()
camera = Camera()

manual_navigator = ManualNavigator(mobile_platform, box_manager)
autonomous_navigator = AutonomousNavigator(mobile_platform, box_manager, modem)

app = Flask(__name__)
socketio = SocketIO(app)

streaming = True

def generate_frames():
    while streaming:
        frame = camera.read_frame()
        unwraped_frame = camera.unwrap_fisheye(frame)
        frame = imutils.resize(unwraped_frame, width=400)

        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            continue

        # Yield the frame in a format suitable for streaming
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_gps_data')
def get_gps_data():
    try:
        modem.open_serial()
        gps_data = modem.read_gps_data()
        modem.close_serial()
        return jsonify({"longitude": gps_data['long'], "latitude": gps_data['lat']})
    except Exception as e:
        return jsonify({"error": str(e)})

@socketio.on('switch_mode')
def switch_mode(mode):
    if mode == 'manual':
        autonomous_navigator.stop()
        manual_navigator.start()
    elif mode == 'automatic':
        manual_navigator.stop()
        autonomous_navigator.start()

@socketio.on('start_journey')
def start_journey(customer_number, route):
    autonomous_navigator.get_destination(route)
    autonomous_navigator.navigate(customer_number)

@socketio.on('open_box')
def open_box():
    box_manager.open_box()

@socketio.on('switch_lights')
def switch_lights():
    manual_navigator.switch_lights()

@socketio.on('stop_motors')
def stop_motors():
    if manual_navigator.is_activated():
        manual_navigator.stop_motors()

@socketio.on('move')
def move(direction):
    if manual_navigator.is_activated():
        if direction == 'F':
            manual_navigator.move_forward()
        elif direction == 'B':
            manual_navigator.move_backward()
        elif direction == 'L':
            manual_navigator.turn_left()
        elif direction == 'R':
            manual_navigator.turn_right()
        elif direction == 'Q':
            manual_navigator.move_left_up()
        elif direction == 'E':
            manual_navigator.move_right_up()
        elif direction == 'Z':
            manual_navigator.move_left_down()
        elif direction == 'C':
            manual_navigator.move_right_down()

@socketio.on('start_streaming')
def start_streaming():
    global streaming = True
    return jsonify({'status': 'Streaming is already in progress'})

@socketio.on('stop_streaming')
def stop_streaming():
    global streaming = False
    return jsonify({'status': 'Streaming stopped'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
