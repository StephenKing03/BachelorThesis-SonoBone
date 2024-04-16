#include <AccelStepper.h>

// Define the motor pins
#define STEP_PIN 2
#define DIR_PIN 3

// Create an instance of the AccelStepper class
AccelStepper stepper(AccelStepper::DRIVER, STEP_PIN, DIR_PIN);

void setup() {
    // Set the maximum speed and acceleration of the stepper motor
    stepper.setMaxSpeed(1000); // Set the maximum speed in steps per second
    stepper.setAcceleration(500); // Set the acceleration in steps per second per second

    // Set the initial speed and direction of the stepper motor
    stepper.setSpeed(500); // Set the initial speed in steps per second
    stepper.setDirection(1); // Set the initial direction (1 for clockwise, -1 for counterclockwise)

    // Enable the stepper motor
    stepper.enableOutputs();
}

void loop() {
    // Move the stepper motor continuously
    stepper.runSpeed();
}