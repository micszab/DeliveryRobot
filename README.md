# Stefan delivery robot
The aim of the project was to develop a prototype of an autonomous parcel delivery robot that can be adapted in last-mile delivery conditions. 

<img src="https://github.com/micszab/DeliveryRobot/assets/46929173/ee841592-fa0e-43ab-9ae1-cfab6a447baa" width="300" height="300">
<img src="https://github.com/micszab/DeliveryRobot/assets/46929173/f0231bac-ded3-40b5-b711-c14012e58d00" width="300" height="300"><br>

Raspberry Pi 4B was used as the computational platform along with a module based on SIM7600G-H, allowing the use of LTE cellular network and collecting GNSS data. A wide-angle camera was used to identify the sidewalk and ultrasonic sensors to detect encountered obstacles. The mobile platform was provided by an Arduino Uno with motor controllers.

The table below contains a list of elements used in the project:

<img src="https://github.com/micszab/DeliveryRobot/assets/46929173/b93c5f0f-c0fe-4d44-8e20-557956731162" width="600" height="400"><br>

A power supply system was designed to power the robot to eliminate the restart of the Raspberry Pi platform caused by a drop in battery voltage after starting the engines and to integrate the necessary elements into one module. Two 18650 lithium-ion 3.7 V batteries connected in series were used to store energy.

<img src="https://github.com/micszab/DeliveryRobot/assets/46929173/850dc703-f64a-4e81-945c-efcb29efd44a" width="800" height="500"><br>
<img src="https://github.com/micszab/DeliveryRobot/assets/46929173/986db494-3a71-4240-9662-c7c72184b657" width="600" height="300"><br>

A lighting control system controlled from the GPIO pin of Raspberry Pi showed on picture below was created.

<img src="https://github.com/micszab/DeliveryRobot/assets/46929173/021d78ba-5281-4b30-b0be-23ee61ac4744" width="300" height="300"><br>

Communication between the computing platform and the mobile platform takes place via the serial port. Data from inertial sensor are read via I2C bus. The camera transmits the image via the CSI interface. The remaining elements use GPIO pins.

<img src="https://github.com/micszab/DeliveryRobot/assets/46929173/5792b005-00a7-4940-9b8b-aa71a0d5b934" width="600" height="300"><br>

As part of the project, a housing with a container for shipments was designed in the Autodesk Fusion 360 CAD program. The design includes mounting holes for: LEDs, distance sensors, camera, antenna, servo, switch, hinge, Raspberry Pi and assembly of the floor plate and upper boards. Maximum dimensions of the shipment 10 x 20 x 20 cm. 

<img src="https://github.com/micszab/DeliveryRobot/assets/46929173/088b973c-29de-4825-b087-d3334aa90ff5" width="600" height="300"><br>

A control interface integrated with Google Maps API was developed, allowing for real-time tracking of the robot's location as well as route planning in interactive mode. Manual control from the website level has been added and video preview from the camera has been provided.

<img src="https://github.com/micszab/DeliveryRobot/assets/46929173/9434c5c1-87c7-459c-933d-d168f2b161f3" width="600" height="500"><br>

Dedicated libraries in Python were created for the computational platform. After pressing the button in the control interface, the request is sent to the server, launching the selected method of the ManualNavigator or AutonomousNavigator class, depending on the selected operating mode. In order to perform the task, the previously mentioned classes communicate with the components responsible for controlling and collecting data from electronic components.

<img src="https://github.com/micszab/DeliveryRobot/assets/46929173/c6ecd584-8c0f-48a5-a9a7-e79525565e85" width="600" height="300"><br>

To derive the movement trajectory for the robot, a Camera class was developed using the cv2 and numpy libraries. Within this class, various methods were incorporated to process the image and generate a movement path aligning with the width of the sidewalk. This involves the expansion of a spherical image using parameters obtained through camera calibration. 

The route is established by subjecting the image to a series of filters. These include color conversion to the HSV space, application of Gaussian blur, creation of a binary mask to eliminate colors unrelated to the sidewalks, and marking contours on the resultant mask. Subsequently, strokes are filtered based on their circumference and length. To enhance the overall smoothness, a moving average is sequentially applied to the selected contours.

<img src="https://github.com/micszab/DeliveryRobot/assets/46929173/81496aca-8395-4d54-9121-c80a1bd98074" width="600" height="800"><br>

The necessary elements of delivering shipments to the customer were taken care of: informing the customer via SMS about departure and arrival at the destination, securing the transported shipment with a code and a pickup procedure.

<img src="https://github.com/micszab/DeliveryRobot/assets/46929173/6ce88999-a2b1-44f2-892e-77cc88f41740" width="200" height="350">
<img src="https://github.com/micszab/DeliveryRobot/assets/46929173/86bb7181-fc12-4958-a165-701a59fe3c3f" width="350" height="350"><br>

Comprehensive tests were conducted, including assessment of positioning accuracy, examining reactions to encountered obstacles and verification of the correctness of route recognition. The test results clearly confirmed the readiness of the designed robot for effective implementation in last-mile deliveries in an urban environment.

<img src="https://github.com/micszab/DeliveryRobot/assets/46929173/f4b7e4ab-8afd-4ad6-bcb8-62e4e14f471c" width="500" height="300"><br>
<img src="https://github.com/micszab/DeliveryRobot/assets/46929173/e26aff9c-60c8-4ddf-aba4-efcccc77be2d" width="700" height="300"><br>
<img src="https://github.com/micszab/DeliveryRobot/assets/46929173/907225ab-0953-40be-9e3b-43ea192b9597" width="700" height="300"><br>

