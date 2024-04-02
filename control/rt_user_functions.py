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

#parallel thread for checking exit (stop)
def start_thread():
    
    exit_thread = threading.Thread(target=check_for_exit_key)
    exit_thread.start()

