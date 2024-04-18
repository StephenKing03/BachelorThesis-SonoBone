#define dirPin 5
#define stepPin 2
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
    int speed = 1000;
    int basespeed = 300;
    int f_factor = 1;
    if (Serial.available()) {

        //read icoming text and transform it
        char buffer[32]; // Buffer to hold incoming data
        Serial.setTimeout(10);
        int length = Serial.readBytesUntil('\n', buffer, sizeof(buffer) - 1);
        buffer[length] = '\0'; // Null-terminate the string
        stepper.runSpeed();
        String command = String(buffer);
        stepper.runSpeed();

        if(command.startsWith("sp")) {
            stepper.setMaxSpeed(10000);
            speed = command.substring(2).toInt();
            stepper.setSpeed(speed);
            // Step the motor with a constant speed as set by setSpeed():
            Serial.println("Speed set to " + String(speed));


        }else if(command.startsWith("init")){

            Serial.println("Initializing stepper");
            stepper.setMaxSpeed(10000);
            stepper.setSpeed(3000);
            unsigned long startTime = millis();
            unsigned long duration = 1000; // 3 seconds
            while (millis() - startTime < duration) {
                stepper.runSpeed();
            }
            stepper.setSpeed(-3000);
            startTime = millis();
            duration = 1000; // 3 seconds
            while (millis() - startTime < duration) {
                stepper.runSpeed();
            }
            stepper.setSpeed(0);
            Serial.println("Stepper initialized");

        }else {

            Serial.println("Invalid command");
        }
        stepper.runSpeed();
    }

    stepper.runSpeed();
        

    
}