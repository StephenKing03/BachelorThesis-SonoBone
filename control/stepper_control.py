import serial
import time
from globals import GlobalState
from globals import RobotStats

#function to be called to set a speed
def command_speed():

    return


# Function to send the integer value to the stepper motor
def send_speed(value):

    
    #port = GlobalState().arduino_port
    port  = serial.Serial(RobotStats().port, 9600)
    # Convert value to message
    message = "sp" + str(value)

    # Convert message to bytes - for sending
    message_bytes = message.encode()

    # Send the bytes over serial
    port.write(message_bytes)

    return


def send_position(value):

    extrusion_speed = RobotStats().extrusion_speed * GlobalState().extrusion_speed_modifier * GlobalState().printspeed_modifier / 100 / 100

    '''test with constant extrusion'''

    if(GlobalState().extrusion_direction != 0 and value == 0):
        send_speed(0)
    elif(GlobalState().extrusion_direction != 1 and value > 0):
        send_speed(extrusion_speed)
    elif(GlobalState().extrusion_direction != -1 and value < 0):
        send_speed(-extrusion_speed)
    '''end test with constant extrusion'''

    return

    # Convert value to message
    message = "p" + str(value) + ";s" + str(extrusion_speed)

    # Convert message to bytes - for sending
    message_bytes = message.encode()

    # Send the bytes over serial
    GlobalState().arduino_port.write(message_bytes)

def retract(direction = -1):

    if direction > 0:
        value = 10
    else:
        value = -10
        
    # Convert value to message
    message = "p" + str(value) + ";s" + str(extrusion_speed)

    # Convert message to bytes - for sending
    message_bytes = message.encode()

    # Send the bytes over serial
    GlobalState().arduino_port.write(message_bytes)

    return

def init_steppers():

    try: 
        #setup port for arduino communication
        GlobalState().arduino_port = serial.Serial(RobotStats().port, 9600)

        #initialization sequence
        message = "init"
        message_bytes = message.encode()
        GlobalState().arduino_port.write(message_bytes)
        print("init sent")
    except serial.SerialException:
        print(f"Could not open port {RobotStats().port}")
    
    return

def read_steppers():

    while True:
        #read from serial port
        message = GlobalState().arduino_port.readline()
        print(message)

    return

def wait_ack():
    
    while True:
        print("wait ack")
        try:
            # Read from serial port
            
            message = GlobalState().arduino_port.readline().decode().strip()
            print(message)
            if message == "ack":
                print("acknowledged init")
                break
        except serial.SerialException:
            print("Could not read from port")
            break


    return

def stop_steppers():

    # Close the serial port when done
    GlobalState().GlobalState().arduino_portclose()
    
    return

def monitor_stepper():
    previous_text = ""
    text = " "
    while True:
        text = GlobalState().arduino_port.readline()
        if previous_text != text:
            GlobalState().terminal_text += text
            previous_text = text
        time.sleep(0.1)


'''
# Configure the serial port
port = serial.Serial('COM26', 9600)  # Replace 'COM3' with the appropriate port name

# Function to send the integer value to the stepper motor
def send_value(value):

    # Convert value to message
    message = "sp" + str(value)

    # Convert message to bytes - for sending
    message_bytes = message.encode()

    # Send the bytes over serial
    port.write(message_bytes)


send_value(0)
print("0 sent")
time.sleep(3)

send_value(1000)
print("1000 sent")
time.sleep(3)
send_value(10000)
print("100000")
time.sleep(3)

# Close the serial port when done
port.close()
'''