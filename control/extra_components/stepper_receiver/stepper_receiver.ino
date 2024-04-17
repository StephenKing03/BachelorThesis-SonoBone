#define dirPin 5
#define stepPin 2
#define motorInterfaceType 1
#include "AccelStepper.h"

// Create a new instance of the AccelStepper class:
AccelStepper stepper = AccelStepper(motorInterfaceType, stepPin, dirPin);

void setup() {
    pinMode(A2, INPUT);
    Serial.begin(9600);
    

    

    stepper.setMaxSpeed(1000);
}

void loop() {
    int speed = 1000;
    if (Serial.available()) {
        String command = Serial.readStringUntil('\n');
        command.trim();

        if (command.startsWith("speed")) {
            speed = command.substring(6).toInt();
            stepper.setSpeed(speed);
            // Step the motor with a constant speed as set by setSpeed():
            
            Serial.println("Speed set to " + String(speed));
        } else {
            Serial.println("Invalid command");
        }
    }
    stepper.runSpeed();
}