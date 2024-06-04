import serial
import time
from globals import GlobalState
from globals import RobotStats
import serial.tools.list_ports

def find_arduino():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        try:
            # Try to open and close the port
            # If it fails, it's not the Arduino
            GlobalState().arduino_port = serial.Serial(port.device, 115200, timeout=1)
            time.sleep(3)
            
            
            # If it succeeds, return the port
            return 
        except serial.SerialException:
            pass

    # If no port was found, return None
    return None

def extrude(distance, speed):

    extrusion_speed = round(speed * RobotStats().extrusion_speed * GlobalState().extrusion_speed_modifier * GlobalState().printspeed_modifier / 100 / 100 /100)

    message = "e" + str(distance) + "s" + str(extrusion_speed)

    message_bytes = message.encode()

    GlobalState().arduino_port.write(message_bytes)


def send_combined_position(base_position, extruder_position, index):
    
    extrusion_speed = round(RobotStats().extrusion_speed * GlobalState().extrusion_speed_modifier * GlobalState().printspeed_modifier / 100 / 100 /100)
    base_speed = round(GlobalState().printspeed_modifier * 0.1,2)
    # Convert value to message
    message = "cb" + str(round(base_position,2)) + "s" + str(round(base_speed,2)) + "e" + str(round(extruder_position,2)) + "t" + str(round(extrusion_speed))+ "i" + str(index)
    
    # Convert message to bytes - for sending
    message_bytes = message.encode()
    
    # Send the bytes over serial
    GlobalState().arduino_port.write(message_bytes)
    print("sent in function: " + str(message))    
    return

def send_base_solo_position(base_position, index):
    
    extrusion_speed = round(RobotStats().extrusion_speed * GlobalState().extrusion_speed_modifier * GlobalState().printspeed_modifier / 100 / 100 /100)
    base_speed = round(GlobalState().printspeed_modifier * 0.1,2)
    # Convert value to message
    message = "b" + str(round(base_position,2)) + "s" + str(base_speed) + "i" + str(index)
    
    # Convert message to bytes - for sending
    message_bytes = message.encode()
    
    # Send the bytes over serial
    GlobalState().arduino_port.write(message_bytes)
    #print("sent in fundction: " + str(message))    
    return


def stop_extrude():

    # Convert value to message
    message = "exstop"

    # Convert message to bytes - for sending
    message_bytes = message.encode()

    # Send the bytes over serial
    GlobalState().arduino_port.write(message_bytes)

    return


def retract_extrude():

    # Convert value to message
    message = "exretract"

    # Convert message to bytes - for sending
    message_bytes = message.encode()

    # Send the bytes over serial
    GlobalState().arduino_port.write(message_bytes)

    return

def engage_extrude():

    # Convert value to message
    message = "exengage"

    # Convert message to bytes - for sending
    message_bytes = message.encode()

    # Send the bytes over serial
    GlobalState().arduino_port.write(message_bytes)

    return

def init_steppers():

    find_arduino()
    if GlobalState().arduino_port is None:
        print("Could not find Arduino")

    try: 
        #setup port for arduino communication
        # Configure the serial port
        #GlobalState().arduino_port = serial.Serial('COM27', 9600)  # Replace 'COM3' with the appropriate port 
        #time.sleep(3)

        #initialization sequence
        message = "init"
        message_bytes = message.encode()
        GlobalState().arduino_port.write(message_bytes)
        print("init sent")
    except serial.SerialException:
        print(f"Could not open port {RobotStats().port}")
    
    return

#not used
def read_steppers():

    while True:
        #read from serial port
        message = GlobalState().arduino_port.readline().decode().strip()

        if(message != ""):
            GlobalState().arduino_info.append(message)
        
        #print("message" + message)
        #print("------" + str(GlobalState().arduino_info))

def wait_init():

    while True:
        print("wait init")
        try:
            # Read from serial port
            message = GlobalState().arduino_port.readline().decode().strip()
            print(message)
            if message == "initialized":
                print("init done")
                return
    
        except serial.SerialException:
            print("Could not read from port")
            break

    return

#answers true if the base has reached the desired position of the corresponding index
def done_arduino(index):

    try:
        # Read from serial port
        message = GlobalState().arduino_port.readline().decode().strip()
        print(message)
        if message == "-done i" + str(index):
            print("arduino done")
            return
        
    except serial.SerialException:
        print("Could not read from port")
        
    return False    
            
        
def reset_pos(theta):

    message = "r" + str(theta)
    
    # Convert message to bytes - for sending
    message_bytes = message.encode()
    
    # Send the bytes over serial
    GlobalState().arduino_port.write(message_bytes)
    #print("sent in fundction: " + str(message))
    
    return



def close_steppers():

    # Close the serial port when done
    GlobalState().GlobalState().arduino_portclose()
    
    return
