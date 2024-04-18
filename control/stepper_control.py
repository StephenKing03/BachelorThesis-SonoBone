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
    message = "s" + str(value)

    # Convert message to bytes - for sending
    message_bytes = message.encode()

    # Send the bytes over serial
    port.write(message_bytes)

    return


def send_position(value):

    extrusion_speed = RobotStats().extrusion_speed * GlobalState().extrusion_speed_modifier * GlobalState().printspeed_modifier / 100 / 100

    '''test with constant extrusion'''
    if(value >= 0):
        send_speed(100)

    if(value < 0):
        send_speed(-100)
    '''end test with constant extrusion'''

    return
    # Convert value to message
    message = "p" + str(value)

    # Convert message to bytes - for sending
    message_bytes = message.encode()

    # Send the bytes over serial
    port.write(message_bytes)

def retract():

    #placeholder

    return

def start_steppers():
    
    #setup port for arduino communication
    GlobalState().arduino_port = serial.Serial(RobotStats().port, 9600)

    #initialization sequence
    message = "init"
    message_bytes = message.encode()
    port.write(message_bytes)
    
    return


def stop_steppers():

    # Close the serial port when done
    GlobalState().port.close()
    return



