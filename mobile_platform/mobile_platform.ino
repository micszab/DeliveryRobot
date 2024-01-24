//DIGITAL
#define L1IN1 13
#define L1IN2 12
#define L1IN3 9
#define L1IN4 8

#define L2IN1 2
#define L2IN2 3
#define L2IN3 4
#define L2IN4 7

//PWM
#define L1ENA 11
#define L1ENB 10

#define L2ENA 5
#define L2ENB 6

class MotorControl {
public:
	MotorControl() {}

	// Initialize pins for front motor
	void setFrontMotor() {
	pinMode (L1IN1, OUTPUT);
	pinMode (L1IN2, OUTPUT);
	pinMode (L1IN3, OUTPUT);
	pinMode (L1IN4, OUTPUT);
	pinMode (L1ENA, OUTPUT);
	pinMode (L1ENB, OUTPUT);
	}

	// Initialize pins for back motor
	void setBackMotor() {
	pinMode (L2IN1, OUTPUT);
	pinMode (L2IN2, OUTPUT);
	pinMode (L2IN3, OUTPUT);
	pinMode (L2IN4, OUTPUT);
	pinMode (L2ENA, OUTPUT);
	pinMode (L2ENB, OUTPUT);
	}

	// Set all pins
	void setPins() {
	setFrontMotor();
	setBackMotor();
	}

  // Motor control functions
	void moveForward() {
	  digitalWrite(L1IN1, HIGH);
	  digitalWrite(L1IN2, LOW);
	  digitalWrite(L1IN3, LOW);
	  digitalWrite(L1IN4, HIGH);
	  digitalWrite(L2IN1, LOW);
	  digitalWrite(L2IN2, HIGH);
	  digitalWrite(L2IN3, HIGH);
	  digitalWrite(L2IN4, LOW);
	}

	void moveBackward() {
	  digitalWrite(L1IN1, LOW);
	  digitalWrite(L1IN2, HIGH);
	  digitalWrite(L1IN3, HIGH);
	  digitalWrite(L1IN4, LOW);
	  digitalWrite(L2IN1, HIGH);
	  digitalWrite(L2IN2, LOW);
	  digitalWrite(L2IN3, LOW);
	  digitalWrite(L2IN4, HIGH);
	}

	void turnLeft() {
	  digitalWrite(L1IN1, LOW);
	  digitalWrite(L1IN2, LOW);
	  digitalWrite(L1IN3, LOW);
	  digitalWrite(L1IN4, HIGH);
	  digitalWrite(L2IN1, LOW);
	  digitalWrite(L2IN2, HIGH);
	  digitalWrite(L2IN3, LOW);
	  digitalWrite(L2IN4, LOW);
	}

	void turnRight() {
	  digitalWrite(L1IN1, HIGH);
	  digitalWrite(L1IN2, LOW);
	  digitalWrite(L1IN3, LOW);
	  digitalWrite(L1IN4, LOW);
	  digitalWrite(L2IN1, LOW);
	  digitalWrite(L2IN2, LOW);
	  digitalWrite(L2IN3, HIGH);
	  digitalWrite(L2IN4, LOW);
	}

	void moveLeftUpper() {
	  digitalWrite(L1IN1, LOW);
	  digitalWrite(L1IN2, LOW);
	  digitalWrite(L1IN3, LOW);
	  digitalWrite(L1IN4, HIGH);
	  digitalWrite(L2IN1, LOW);
	  digitalWrite(L2IN2, HIGH);
	  digitalWrite(L2IN3, HIGH);
	  digitalWrite(L2IN4, LOW);
	}

	void moveLeftLower() {
	  digitalWrite(L1IN1, LOW);
	  digitalWrite(L1IN2, LOW);
	  digitalWrite(L1IN3, HIGH);
	  digitalWrite(L1IN4, LOW);
	  digitalWrite(L2IN1, HIGH);
	  digitalWrite(L2IN2, LOW);
	  digitalWrite(L2IN3, LOW);
	  digitalWrite(L2IN4, HIGH);
	}

	void moveRightUpper() {
	  digitalWrite(L1IN1, HIGH);
	  digitalWrite(L1IN2, LOW);
	  digitalWrite(L1IN3, LOW);
	  digitalWrite(L1IN4, LOW);
	  digitalWrite(L2IN1, LOW);
	  digitalWrite(L2IN2, HIGH);
	  digitalWrite(L2IN3, HIGH);
	  digitalWrite(L2IN4, LOW);
	}

	void moveRightLower() {
	  digitalWrite(L1IN1, LOW);
	  digitalWrite(L1IN2, HIGH);
	  digitalWrite(L1IN3, LOW);
	  digitalWrite(L1IN4, LOW);
	  digitalWrite(L2IN1, HIGH);
	  digitalWrite(L2IN2, LOW);
	  digitalWrite(L2IN3, LOW);
	  digitalWrite(L2IN4, HIGH);
	}

  // Stop all motors
	void stopMotors() {
	digitalWrite(L1IN1, LOW);
	digitalWrite(L1IN2, LOW);
	digitalWrite(L1IN3, LOW);
	digitalWrite(L1IN4, LOW);
	digitalWrite(L2IN1, LOW);
	digitalWrite(L2IN2, LOW);
	digitalWrite(L2IN3, LOW);
	digitalWrite(L2IN4, LOW);
	}

	// Control motor direction based on command
	void controlDirection(char command) {
	switch (command) {
		case 'F':
		  moveForward();
		  break;

		case 'B':
		  moveBackward();
		  break;

		case 'L':
		  turnLeft();
		  break;

		case 'R':
		  turnRight();
		  break;

		case 'Q':
		  moveLeftUpper();
		  break;

		case 'Z':
		  moveLeftLower();
		  break;

		case 'E':
		  moveRightUpper();
		  break;

		case 'C':
		  moveRightLower();
		  break;

		case 'S':
		  stopMotors();
		  break;

		default:
		  stopMotors();
		  break;
	}
	}

	// Control motor speed
	void controlSpeed(int speed_value) {  
	analogWrite(L1ENA, speed_value);
	analogWrite(L1ENB, speed_value); 
	analogWrite(L2ENA, speed_value);
	analogWrite(L2ENB, speed_value); 
	}
};

MotorControl motorControl;

void setSerial() {
  Serial.begin(115200);
}

void setup() {
  motorControl.setPins();
  setSerial();
}

void loop() {
  readSerialPort();
  delay(500);
}

void readSerialPort() {
  if (Serial.available()) {
    char startMarker = '<';
    char endMarker = '>';
    char direction;
    int value;

    if (Serial.read() == startMarker) {
      direction = Serial.read();
      value = Serial.parseInt();
      
      motorControl.controlDirection(direction);
      motorControl.controlSpeed(value);
      
      while (Serial.read() != endMarker) {
      }
      
    Serial.flush();
    }
  }
}

