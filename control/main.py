import gui
import threading
import time
import logging
from globals import GlobalState
import mecademicpy.robot as mdr #mechademicpy API import (see Github documentation)

def init_logger():

    old_terminal_text = GlobalState().terminal_text
    while True:
        if GlobalState().terminal_text != old_terminal_text:
            lines = GlobalState().terminal_text.split('\n')
            last_line = lines[len(lines)-2]
            current_time = datetime.now().time()
            current_time_string = current_time.strftime("%H:%M:%S")
            # If terminal_text has changed, log the new value
            logging.info(current_time_string + ": " + last_line + "\n")
            old_terminal_text = GlobalState().terminal_text
            time.sleep(0.5)
    return


#logging thread:
logging.basicConfig(filename='terminal_text.log', level=logging.INFO, format='%(asctime)s %(message)s')
logging_thread = threading.Thread(target=init_logger)
# - en or disable the logging
#logging_thread.start()

#main program
gui.init_gui()