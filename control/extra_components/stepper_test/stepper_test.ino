#define dirPin 5
#define stepPin 2
#define motorInterfaceType 1
#include "AccelStepper.h"

// Create a new instance of the AccelStepper class:
AccelStepper stepper = AccelStepper(motorInterfaceType, stepPin, dirPin);

int input;

void setup() {
  pinMode(A2, INPUT);
  Serial.begin(9600);
  
  input = 0;

  // Set the maximum speed in steps per second:
  stepper.setMaxSpeed(1000);
}

void loop() {
  // Set the speed in steps per second:
  
// Set the speed in steps per second:
  stepper.setSpeed(1000);
  // Step the motor with a constant speed as set by setSpeed():
  stepper.runSpeed();
  
  // wait for 1 second:
  

  
}