import gui
import threading
import time
import logging
from globals import GlobalState
import mecademicpy.robot as mdr #mechademicpy API import (see Github documentation)
import utility_functions as uf

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


GlobalState().msb = mdr.Robot() #msb = MegaSonoBot # instance of the robot class
GlobalState().msb.Connect(address='192.168.0.100') #using IP address of the robot and Port 10000 to control
GlobalState().msb.ActivateRobot() #same as in the webinterface: activate Robot
GlobalState().msb.Home() #Home the robot
GlobalState().msb.SendCustomCommand("SetRealTimeMonitoring('cartpos')") #start logging position
GlobalState().msb.WaitIdle()
with GlobalState().msb.FileLogger(0.001, fields =['CartPos']):
    GlobalState().msb.MoveJoints(30, -60, 60, 0, 0, 0)
    GlobalState().msb.MoveJoints(0, -60, 60, 0, 0, 0)
    #print(uf.GetPose(GlobalState().msb))
    GlobalState().msb.MoveJoints(0, 0, 0, 0, 0, 0)
    GlobalState().msb.WaitIdle()





#logging thread:
logging.basicConfig(filename='terminal_text.log', level=logging.INFO, format='%(asctime)s %(message)s')
logging_thread = threading.Thread(target=init_logger)
# - en or disable the logging
#logging_thread.start()

#main program
gui.init_gui()