#define dirPin 6
#define stepPin 3
#define motorInterfaceType 1
#include "AccelStepper.h"

// Create a new instance of the AccelStepper class:
AccelStepper stepper = AccelStepper(motorInterfaceType, stepPin, dirPin);

void setup() {
    pinMode(A2, INPUT);
    Serial.begin(9600);
    
    stepper.setMaxSpeed(10000);
    
}

void loop() {
    

    
    stepper.setSpeed(1000);
    
    stepper.runSpeed();
        

    
}