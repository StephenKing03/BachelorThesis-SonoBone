#define dirPin 6
#define stepPin 3
#define motorInterfaceType 1
#include "AccelStepper.h"
int i = 0;

// Create a new instance of the AccelStepper class:
AccelStepper stepper = AccelStepper(motorInterfaceType, stepPin, dirPin);

void setup() {
    pinMode(A2, INPUT);
    Serial.begin(9600);
    
    stepper.setMaxSpeed(100);
    stepper.setAcceleration(50000);

    

    
}

void loop() {
            i = i+1;
 // calculate the number of steps required to move the specified distance
            float distanceInDeg = 360;
            float degPerStep = 1.8; // Adjust this value based on your stepper motor specifications
            int steps = distanceInDeg / degPerStep;

            
            //set the speed in steps per second
            
            stepper.moveTo(steps);
            stepper.setSpeed(1000);
            

            unsigned long startTime = millis();
            unsigned long timeout = 10000; // 3 seconds

            
            while(stepper.distanceToGo() >= 1){
                stepper.run();
            }
            stepper.setSpeed(0);
            
    
}