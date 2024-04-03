import keyboard
import time
from globals import GlobalState
from globals import RobotStats
import threading
import utility_functions as uf


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
def start_thread():
    
    exit_thread = threading.Thread(target=check_for_exit_key)
    exit_thread.start()
    z_tune_thread = threading.Thread(target=z_tuning)
    z_tune_thread.start()



