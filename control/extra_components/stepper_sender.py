import serial

# Define the serial port and baud rate
port = 'COM3'  # Replace with the appropriate port name
baud_rate = 9600  # Replace with the appropriate baud rate

# Create a serial connection
ser = serial.Serial(port, baud_rate)

# Function to send speed to Arduino
def send_speed(speed):
    # Convert the speed to bytes
    speed_bytes = str(speed).encode('utf-8')
    
    # Send the speed over serial
    ser.write(speed_bytes)
    
# Example usage
speed = 50  # Replace with the desired speed value
send_speed(speed)

# Close the serial connection
ser.close()