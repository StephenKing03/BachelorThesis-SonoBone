import gui
import threading
import time
import logging
from globals import GlobalState
from globals import RobotStats
import mecademicpy.robot as mdr #mechademicpy API import (see Github documentation)
import utility_functions as uf
'''
def init_logger():

    old_terminal_text = GlobalState().terminal_text
    while True:


        if(GlobalState().terminal_text == last_text):
            continue
        if GlobalState().terminal_text != "":
            #get timestamp
            current_time = datetime.now().time()    
            current_time_string = current_time.strftime("%H:%M:%S") 

            #print line with timestamp
            text = GlobalState().terminal_text
    
    
            #remove the text
            GlobalState().terminal_text = ""
            
            #print only the stuff that does not already exist
            logging.info(current_time_string + ": " + text + "\n")
            
            last_text = text
  
  
            #scroll to the end
            last_index = i
        time.sleep(0.005)
 
    return

#logging test

#custom logging thread:
#logging.basicConfig(filename='terminal_text.log', level=logging.INFO, format='%(asctime)s %(message)s')
#logging_thread = threading.Thread(target=init_logger)
# - en or disable the logging
#logging_thread.start()

'''


#---------------main program start------------
RobotStats().portname = "COM3"
gui.init_gui()