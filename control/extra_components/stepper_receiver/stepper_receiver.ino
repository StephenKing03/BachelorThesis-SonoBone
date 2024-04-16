#include <Stepper.h>

// Define the number of steps per revolution
const int stepsPerRevolution = 200;

// Create a Stepper object
Stepper myStepper(stepsPerRevolution, 8, 9, 10, 11);

void setup() {
  // Initialize the serial communication
  Serial.begin(9600);
}

void loop() {
  // Check if there is any data available to read from the serial port
  if (Serial.available() > 0) {
    // Read the incoming value as an integer
    int speed = Serial.parseInt();
    speed = 1000;

    // Set the motor speed
    myStepper.setSpeed(speed);

    // Rotate the motor continuously
    myStepper.step(stepsPerRevolution);
  }
}