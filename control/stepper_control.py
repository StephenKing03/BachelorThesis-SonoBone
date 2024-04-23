import serial
import time
from globals import GlobalState
from globals import RobotStats

#function to be called to set a speed
def command_speed():

    return


# Function to send the integer value to the stepper motor
def send_speed(value):

    # Convert value to message
    message = "sp" + str(value)

    # Convert message to bytes - for sending
    message_bytes = message.encode()

    # Send the bytes over serial
    GlobalState().arduino_port.write(message_bytes)

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
    
    #setup port for arduino communication
    GlobalState().arduino_port = serial.Serial(RobotStats().port, 9600)

    #initialization sequence
    message = "init"
    message_bytes = message.encode()
    GlobalState().arduino_port.write(message_bytes)
    
    return

def read_steppers():

    while True:
        #read from serial port
        message = GlobalState().arduino_port.readline()
        print(message)

    return

def wait_ack():
    
        while True:
            #read from serial port
            message = GlobalState().arduino_port.readline()
            if message == "ack":
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



