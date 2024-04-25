import serial
import time

# Configure the serial port
port = serial.Serial('COM27', 9600)  # Replace 'COM3' with the appropriate port name

# Function to send the integer value to the stepper motor
def send_value(value):

    # Convert value to message
    message = "sp" + str(value)

    # Convert message to bytes - for sending
    message_bytes = message.encode()

    # Send the bytes over serial
    port.write(message_bytes)


# Example usage
for i in range (10):
    for i in range(0,10000,1000):
        send_value(i)
        print(i)
        time.sleep(3)
value = 100  # Replace with your desired integer value
send_value(value)

# Close the serial port when done
port.close()