import keyboard
import time
from globals import GlobalState
import threading
import utility_functions as uf

def check_for_exit_key():
    
    while True:
        if keyboard.is_pressed('x'):
            print("Program stopped by user - ef")
            GlobalState().exit_program = True
            time.sleep(2)
            break
    print("deactivating robot")
    uf.cleanpose()
    uf.clean_motion()
    #while True:
        #time.sleep(0.2)
        #print(f'exit_program ------- ruf: {GlobalState().exit_program}')
           

    return False

#parallel thread for checking exit (stop)
def check_for_exit():
    
    exit_thread = threading.Thread(target=check_for_exit_key)
    exit_thread.start()

