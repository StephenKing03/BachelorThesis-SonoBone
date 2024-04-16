#include <AccelStepper.h>
#include <SoftwareSerial.h>

// Define the stepper motor pins
#define STEP_PIN 3
#define DIR_PIN 6

// Define the serial communication pins
#define RX_PIN 10
#define TX_PIN 11

// Create a SoftwareSerial object for serial communication
SoftwareSerial serial(RX_PIN, TX_PIN);

// Create an AccelStepper object for controlling the stepper motor
AccelStepper stepper(AccelStepper::DRIVER, STEP_PIN, DIR_PIN);

void setup() {
    // Set the baud rate for serial communication
    serial.begin(9600);

    // Set the maximum speed and acceleration of the stepper motor
    stepper.setMaxSpeed(1000);
    stepper.setAcceleration(500);
}

void loop() {
    // Check if there is any data available to read from serial
    if (serial.available()) {
        // Read the speed command from serial
        int speed = serial.parseInt();

        // Set the speed of the stepper motor
        stepper.setSpeed(speed);

        // Move the stepper motor continuously
        stepper.runSpeed();
    }
}