import keyboard
import time
from globals import GlobalState
from globals import RobotStats
import threading
import utility_functions as uf
import gcode_translator as gt #import gcode translator

def start_printing():
    #check if file path is set:
    if GlobalState().filepath == " ":
        print("No file path set")
        GlobalState().start_printing = False
        return False
    gt.write_coordinates(gt.extract_coordinates(GlobalState().filepath), msb)
    return True


#check for the exot key 'x' to stop the program
def check_for_exit_key():
    
    while True:
        if keyboard.is_pressed('x'):
            print("Program stopped by user - ef")
            GlobalState().exit_program = True
            break

    print("deactivating robot")
    uf.endpose()
    uf.clean_motion()
    uf.deactivationsequence()
    
    return False


def z_tuning():
        offset_interval = 0.15
        while True:
            if keyboard.is_pressed('i'):
                print("w pressed")
                GlobalState().user_z_offset += offset_interval
                print(f"offset: now", {GlobalState().user_z_offset})
               
            elif keyboard.is_pressed('k'):
                print("s pressed")
                GlobalState().user_z_offset -= offset_interval
                print(f"offset:  now", {GlobalState().user_z_offset})


        return False


#parallel thread for checking exit (stop) and tuning of z_offset
def start_threads():
    
    exit_thread = threading.Thread(target=check_for_exit_key)
    exit_thread.start()
    z_tune_thread = threading.Thread(target=z_tuning)
    z_tune_thread.start()

def main_program():

    start_thread()

    #wait for start signal and then initiate robot
    while(not GlobalState().startProgram):
        time.sleep(0.1)
    msb = uf.activationsequence()

    #wait for start signal and then initiate robot
    while(not GlobalState().startProgram):
        time.sleep(0.1)
    
    


    



