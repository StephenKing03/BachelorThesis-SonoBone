import keyboard
import time
from globals import GlobalState
from globals import RobotStats
import threading
import utility_functions as uf
import gcode_translator as gt #import gcode translator

#check for the exot key 'x' to stop the program
def check_for_exit_key():
    
    while True:
        if keyboard.is_pressed('x'):
            print("Program stopped by user - ef")
            GlobalState().terminal_text += "program was stopped by user pressing 'X'\n"
            GlobalState().exit_program = True
            break

    print("deactivating robot")
    uf.endpose()
    uf.clean_motion()
    uf.deactivationsequence()
    
    return False



#depracated
def z_tuning():
        offset_interval = GlobalState().user_z_offset_increment
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
    
    #exit_thread = threading.Thread(target=check_for_exit_key)
    #exit_thread.start()
    #z_tune_thread = threading.Thread(target=z_tuning)
    #z_tune_thread.start()
    #speed_thread = threading.Thread(target=speed_tuning)
    #speed_thread.start()
    return

def main_program():

    start_threads()

    return
    
    


    



