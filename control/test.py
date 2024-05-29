import stepper_control as sc
import time
from globals import GlobalState
import threading

def send_combined_position(base_position, index):
    
    extrusion_speed = 10
    base_speed = 10
    # Convert value to message
    message = "c" + str(extrusion_speed) + "b" + str(base_position) + "s" + str(base_speed) + "i" + str(index)
    
    # Convert message to bytes - for sending
    message_bytes = message.encode()
    
    # Send the bytes over serial
    GlobalState().arduino_port.write(message_bytes)
    print("sent in fundction: " + str(message))
    
    return


sc.init_steppers()
sc.wait_init()

arduino_thread = threading.Thread(target= sc.read_steppers)
arduino_thread.start()

time.sleep(2)
send_combined_position(30, 1)

while sc.done_base(1) == False:
    time.sleep(0.1)

print("prgram done")
