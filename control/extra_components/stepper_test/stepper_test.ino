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

   // Set the speed in steps per second:
  
// Set the speed in steps per second:

// Calculate the number of steps required to move 10mm
float distanceInMM = 100.0;
float stepsPerMM = 100.0; // Adjust this value based on your stepper motor specifications
int steps = distanceInMM * stepsPerMM;

// Set the desired speed in steps per second
float speedInMMPerSec = 5.0; // Adjust this value to set the speed
float speedInStepsPerSec = speedInMMPerSec * stepsPerMM;
stepper.setSpeed(speedInStepsPerSec);
  stepper.setMaxSpeed(10000);

// Move the stepper motor by the specified number of steps
//stepper.moveTo(steps);

stepper.setSpeed(1000);
stepper.setAcceleration(50000);
stepper.moveTo(2048);
  

  // Set the maximum speed in steps per second:

}

void loop() {
 
stepper.run();
if(stepper.distanceToGo() == 0){
Serial.println("Hurray");
}

}